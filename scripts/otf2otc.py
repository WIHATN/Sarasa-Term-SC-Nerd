# otf2otc.py v1.5 October 12 2017

__copyright__ = """Copyright 2014,2017 Adobe Systems Incorporated (http://www.adobe.com/). All Rights Reserved.
"""

import sys
import os
import struct

class OTCError(TypeError):
	pass

class FontEntry:
	def __init__(self, sfntType, searchRange, entrySelector, rangeShift):
		self.sfntType = sfntType
		self.searchRange = searchRange
		self.entrySelector = entrySelector
		self.rangeShift = rangeShift
		self.tableList = []

	def append(self, tableEntry):
		self.tableList.append(tableEntry)

	def getTable(self, tableTag):
		for tableEntry in self.tableList:
			if tableTag == tableEntry.tag:
				return tableEntry
		raise KeyError("Failed to find tag: " + tableTag)

class TableEntry:
	def __init__(self, tag, checkSum, length):
		self.tag = tag
		self.checksum = checkSum
		self.length = length
		self.data = None
		self.offset = None

ttcHeaderFormat = ">4sLL"
ttcHeaderSize = struct.calcsize(ttcHeaderFormat)
offsetFormat = ">L"
offsetSize = struct.calcsize(">L")
sfntDirectoryFormat = ">4sHHHH"
sfntDirectorySize = struct.calcsize(sfntDirectoryFormat)
sfntDirectoryEntryFormat = ">4sLLL"
sfntDirectoryEntrySize = struct.calcsize(sfntDirectoryEntryFormat)

def parseArgs(args):
	tagOverrideMap = {}
	ttcFilePath = "TempTTC.ttc"
	fontList = []
	argn = len(args)
	i = 0
	while i < argn:
		arg = args[i]
		i += 1
		if arg[0] != '-':
			fontList.append(arg)
		elif arg == "-o":
			ttcFilePath = args[i]
			i += 1
		elif arg == "-t":
			parts = args[i].split("=")
			try:
				tag = parts[0].strip("\"'")
				fontIndex = int(parts[1])
			except (ValueError, IndexError):
				raise OTCError("Badly formed table override.")
			tagOverrideMap[bytes(tag, 'ascii')] = fontIndex
			i += 1
		else:
			raise OTCError("Unknown option '%s'." % (arg))
	if len(fontList) < 1:
		raise OTCError("You must specify at least one input font.")
	for fontPath in fontList:
		if not os.path.exists(fontPath):
			raise OTCError("Cannot find '%s'." % (fontPath))
	return tagOverrideMap, fontList, ttcFilePath

def readFontFile(fontPath):
	fontEntryList = []
	with open(fontPath, "rb") as fp:
		data = fp.read()
	TTCTag, version, numFonts = struct.unpack(ttcHeaderFormat, data[:ttcHeaderSize])
	if TTCTag != b'ttcf':
		fontEntryList.append(parseFontFile(0, data))
	else:
		offsetdata = data[ttcHeaderSize:]
		for _ in range(numFonts):
			offset = struct.unpack(offsetFormat, offsetdata[:offsetSize])[0]
			fontEntryList.append(parseFontFile(offset, data))
			offsetdata = offsetdata[offsetSize:]
	return fontEntryList

def parseFontFile(offset, data):
	sfntType, numTables, searchRange, entrySelector, rangeShift = struct.unpack(sfntDirectoryFormat, data[offset:offset+sfntDirectorySize])
	fontEntry = FontEntry(sfntType, searchRange, entrySelector, rangeShift)
	curData = data[offset+sfntDirectorySize:]
	for _ in range(numTables):
		tag, checkSum, toffset, length = struct.unpack(sfntDirectoryEntryFormat, curData[:sfntDirectoryEntrySize])
		tableEntry = TableEntry(tag, checkSum, length)
		tableEntry.data = data[toffset:toffset+length]
		fontEntry.append(tableEntry)
		curData = curData[sfntDirectoryEntrySize:]
	return fontEntry

def writeTTC(fontList, tableList, ttcFilePath):
	numFonts = len(fontList)
	header = struct.pack(ttcHeaderFormat, b'ttcf', 0x00010000, numFonts)
	dataList = [header]
	fontOffset = ttcHeaderSize + numFonts * struct.calcsize(">L")
	for fontEntry in fontList:
		dataList.append(struct.pack(">L", fontOffset))
		fontOffset += sfntDirectorySize + len(fontEntry.tableList) * sfntDirectoryEntrySize
	for tableEntryList in tableList:
		for tableEntry in tableEntryList:
			tableEntry.offset = fontOffset
			paddedLength = (tableEntry.length + 3) & ~3
			fontOffset += paddedLength
	for fontEntry in fontList:
		data = struct.pack(sfntDirectoryFormat, fontEntry.sfntType, len(fontEntry.tableList), fontEntry.searchRange, fontEntry.entrySelector, fontEntry.rangeShift)
		dataList.append(data)
		for tableEntry in fontEntry.tableList:
			data = struct.pack(sfntDirectoryEntryFormat, tableEntry.tag, tableEntry.checksum, tableEntry.offset, tableEntry.length)
			dataList.append(data)
	for tableEntryList in tableList:
		for tableEntry in tableEntryList:
			paddedLength = (tableEntry.length + 3) & ~3
			paddedData = tableEntry.data + b"\0" * (paddedLength - tableEntry.length)
			dataList.append(paddedData)
	with open(ttcFilePath, "wb") as fp:
		fp.write(b"".join(dataList))

def run(args):
	tagOverrideMap, fileList, ttcFilePath = parseArgs(args)
	print("Input fonts:", fileList)
	fontList = []
	tableMap = {}
	tableList = []
	for fontPath in fileList:
		fontList += readFontFile(fontPath)
	for fontEntry in fontList:
		for tableIndex in range(len(fontEntry.tableList)):
			tableEntry = fontEntry.tableList[tableIndex]
			try:
				fontIndex = tagOverrideMap[tableEntry.tag]
				tableEntry = fontList[fontIndex].getTable(tableEntry.tag)
				fontEntry.tableList[tableIndex] = tableEntry
			except KeyError:
				pass
			try:
				tableEntryList = tableMap[tableEntry.tag]
				matched = 0
				for tEntry in tableEntryList:
					if (tEntry.checksum == tableEntry.checksum) and (tEntry.length == tableEntry.length) and (tEntry.data == tableEntry.data):
						matched = 1
						fontEntry.tableList[tableIndex] = tEntry
						break
				if not matched:
					tableEntryList.append(tableEntry)
			except KeyError:
				tableEntryList = [tableEntry]
				tableMap[tableEntry.tag] = tableEntryList
				tableList.insert(tableIndex, tableEntryList)
	writeTTC(fontList, tableList, ttcFilePath)
	print("Output font:", ttcFilePath)
	print("Done")

def main():
	try:
		run(sys.argv[1:])
	except OTCError as e:
		print(e)

if __name__ == "__main__":
	main()
