##################################################################################
# Dynamic Audio Normalizer - Python Wrapper
# Copyright (c) 2014-2017 LoRd_MuldeR <mulder2@gmx.de>. Some rights reserved.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# http://opensource.org/licenses/MIT
##################################################################################

#import stdlib modules
import sys

#define API version
DYNAMIC_AUDIONORMALIZER_API = 8

#import the native "C" module
try:
	import DynamicAudioNormalizerAPI
except:
	pass

#error checking
if (not 'DynamicAudioNormalizerAPI' in locals()) or (not hasattr(DynamicAudioNormalizerAPI, 'getCoreVersion')):
	raise SystemError("The native DynamicAudioNormalizerAPI module is *not* available. Please make sure that 'DynamicAudioNormalizerAPI.pyd' has been installed correctly!")

#version checking
if DynamicAudioNormalizerAPI.getCoreVersion() != DYNAMIC_AUDIONORMALIZER_API:
	raise SystemError("The native DynamicAudioNormalizerAPI module uses an *unsupported* API version. Please install the matching 'DynamicAudioNormalizerAPI.pyd' library!")


#----------------------------------------------------------------------
# DynamicAudioNormalizer
#----------------------------------------------------------------------

class DynamicAudioNormalizer:
	"""Wrapper class around the DynamicAudioNormalizerAPI library"""
	
	def __str__(self):
		versionInfo = self.getVersion()
		buildStr = "built: {} {}, compiler: {}, arch: {}, {}".format(*versionInfo[1])
		configStr = "channels={}, samplingRate={}, frameLen={}, filterSize={}".format(*self.getConfig())
		return "DynamicAudioNormalizer v{}.{}-{} [{}][{}]]".format(*versionInfo[0], buildStr, configStr)
	
	def __init__(self, channels, samplerate, filterSize=31, frameLen=500, peakValue=0.95, maxAmplification=10.0, targetRms=0.0, compressFactor=0.0, channelsCoupled=True, enableDCCorrection=False, altBoundaryMode=False):
		self._channels = int(channels)
		self._samplerate = int(samplerate)
		self._frameLen = int(frameLen)
		self._filterSize = int(filterSize)
		self._peakValue = float(peakValue)
		self._maxAmplification = float(maxAmplification)
		self._targetRms = float(targetRms)
		self._compressFactor = float(compressFactor)
		self._channelsCoupled = not (not channelsCoupled)
		self._enableDCCorrection = not (not enableDCCorrection)
		self._altBoundaryMode = not (not altBoundaryMode)
		self._instance = None
	
	def __enter__(self):
		options = (self._peakValue, self._maxAmplification, self._targetRms, self._compressFactor, self._channelsCoupled, self._enableDCCorrection, self._altBoundaryMode)
		self._instance = DynamicAudioNormalizerAPI.create(self._channels, self._samplerate, self._frameLen, self._filterSize, *options)
		return self
	
	def __exit__(self, type, value, traceback):
		if not self._instance:
			raise RuntimeError("Instance not initialized!")
		DynamicAudioNormalizerAPI.destroy(self._instance)
		self._instance = None
	
	def __del__(self):
		if self._instance:
			print("RESOURCE LEAK: DynamicAudioNormalizer object was not de-initialized properly!", file=sys.stderr)
	
	def getConfig(self):
		if not self._instance:
			raise RuntimeError("Instance not initialized!")
		return DynamicAudioNormalizerAPI.getConfig(self._instance)
	
	def processInplace(self, samplesInOut, count):
		if not self._instance:
			raise RuntimeError("Instance not initialized!")
		return DynamicAudioNormalizerAPI.processInplace(self._instance, samplesInOut, count)
	
	def flushBuffer(self, samplesOut):
		if not self._instance:
			raise RuntimeError("Instance not initialized!")
		return DynamicAudioNormalizerAPI.flushBuffer(self._instance, samplesOut)
	
	@staticmethod
	def getVersion():
		return DynamicAudioNormalizerAPI.getVersionInfo()

