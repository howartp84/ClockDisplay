#! /usr/bin/env python
# -*- coding: utf-8 -*-
####################
# Copyright (c) 2016, Perceptive Automation, LLC. All rights reserved.
# http://www.indigodomo.com

import indigo

import os
import sys

import time
import datetime

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)

	def closedPrefsConfigUi(self, valuesDict, userCancelled):
		# Since the dialog closed we want to set the debug flag - if you don't directly use
		# a plugin's properties (and for debugLog we don't) you'll want to translate it to
		# the appropriate stuff here.
		if not userCancelled:
			self.useSeconds = valuesDict.get("useSeconds", False)
		return True
		
	def deviceStartComm(self, dev):
		dev.stateListOrDisplayStateIdChanged()
		self.sleepTime = 30

	def runConcurrentThread(self):
		try:
			while True:
			
				for d in indigo.devices.iter("self.clockdisplay"):
					key_value_list = [
					#if (time.strftime("%d/%m/%y") != d.states["DateUK_DDMMYY"]):
						#indigo.server.log("New Day")
					{"key":"DateUK_DDMMYY","value":time.strftime("%d/%m/%y")},
					{"key":"DateUK_DDMMYYYY","value":time.strftime("%d/%m/%Y")},
					{"key":"DateUS_MMDDYY","value":time.strftime("%m/%d/%y")},
					{"key":"DateUS_MMDDYYYY","value":time.strftime("%m/%d/%Y")},
					{"key":"Day_Long","value":time.strftime("%A")},
					{"key":"Day_Short","value":time.strftime("%a")},
					{"key":"LocalDate","value":time.strftime("%x")},
					{"key":"Time_12HHMM","value":time.strftime("%-I:%M")},
					{"key":"Time_12HHMMSS","value":time.strftime("%-I:%M:%S")},
					{"key":"Time_24HHMM","value":time.strftime("%-H:%M")},
					{"key":"Time_24HHMMSS","value":time.strftime("%-H:%M:%S")},
					{"key":"Time_12HHMMAMPM","value":time.strftime("%-I:%M%p")},
					{"key":"Time_12HHMMSSAMPM","value":time.strftime("%-I:%M:%S%p")},
					{"key":"Time_24HHMMAMPM","value":time.strftime("%-H:%M%p")},
					{"key":"Time_24HHMMSSAMPM","value":time.strftime("%-H:%M:%S%p")},
					{"key":"Time_12HHMMAMPML","value":time.strftime("%-I:%M%p").lower()},
					{"key":"Time_12HHMMSSAMPML","value":time.strftime("%-I:%M:%S%p").lower()},
					{"key":"Time_24HHMMAMPML","value":time.strftime("%-H:%M%p").lower()},
					{"key":"Time_24HHMMSSAMPML","value":time.strftime("%-H:%M%p").lower()},
					{"key":"Time_12HMM","value":time.strftime("%I:%M")},
					{"key":"Time_12HMMSS","value":time.strftime("%I:%M:%S")},
					{"key":"Time_24HMM","value":time.strftime("%H:%M")},
					{"key":"Time_24HMMSS","value":time.strftime("%H:%M:%S")},
					{"key":"Time_12HMMAMPM","value":time.strftime("%I:%M%p")},
					{"key":"Time_12HMMSSAMPM","value":time.strftime("%I:%M:%S%p")},
					{"key":"Time_24HMMAMPM","value":time.strftime("%H:%M%p")},
					{"key":"Time_24HMMSSAMPM","value":time.strftime("%H:%M:%S%p")},
					{"key":"Time_12HMMAMPML","value":time.strftime("%I:%M%p").lower()},
					{"key":"Time_12HMMSSAMPML","value":time.strftime("%I:%M:%S%p").lower()},
					{"key":"Time_24HMMAMPML","value":time.strftime("%H:%M%p").lower()},
					{"key":"Time_24HMMSSAMPML","value":time.strftime("%H:%M%p").lower()},
					{"key":"LocalTime","value":time.strftime("%X")},
					{"key":"Custom1","value":time.strftime(d.ownerProps.get("custom1",""))},
					{"key":"Custom2","value":time.strftime(d.ownerProps.get("custom2",""))},
					{"key":"Custom3","value":time.strftime(d.ownerProps.get("custom3",""))},
					{"key":"Custom4","value":time.strftime(d.ownerProps.get("custom4",""))},
					{"key":"Custom5","value":time.strftime(d.ownerProps.get("custom5",""))},
					]
					d.updateStatesOnServer(key_value_list)
		
					if (d.ownerProps.get("useSeconds",False)): #True
						self.sleepTime = 1
				
				self.sleep(self.sleepTime)
		except self.StopThread:
			pass
