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

	def runConcurrentThread(self):
		try:
			while True:
			
				for d in indigo.devices.iter("self.clockdisplay"):
					if (time.strftime("%d/%m/%y") != d.states["DateUK_DDMMYY"]):
						indigo.server.log("New Day")
						d.updateStateOnServer("DateUK_DDMMYY",time.strftime("%d/%m/%y"))
						d.updateStateOnServer("DateUK_DDMMYYYY",time.strftime("%d/%m/%Y"))
						d.updateStateOnServer("DateUS_MMDDYY",time.strftime("%m/%d/%y"))
						d.updateStateOnServer("DateUS_MMDDYYYY",time.strftime("%m/%d/%Y"))
						d.updateStateOnServer("Day_Long",time.strftime("%A"))
						d.updateStateOnServer("Day_Short",time.strftime("%a"))
						d.updateStateOnServer("LocalDate",time.strftime("%x"))
					d.updateStateOnServer("Time_12HHMM",time.strftime("%I:%M"))
					d.updateStateOnServer("Time_12HHMMSS",time.strftime("%I:%M:%S"))
					d.updateStateOnServer("Time_24HHMM",time.strftime("%H:%M"))
					d.updateStateOnServer("Time_24HHMMSS",time.strftime("%H:%M:%S"))
					d.updateStateOnServer("Time_12HHMMAMPM",time.strftime("%I:%M %p"))
					d.updateStateOnServer("Time_12HHMMSSAMPM",time.strftime("%I:%M:%S %p"))
					d.updateStateOnServer("Time_24HHMMAMPM",time.strftime("%H:%M %p"))
					d.updateStateOnServer("Time_24HHMMSSAMPM",time.strftime("%H:%M:%S %p"))
					d.updateStateOnServer("LocalTime",time.strftime("%X"))
		
					if (d.ownerProps.get("useSeconds",False)): #True
						self.sleep(1) # in seconds
					else:
						self.sleep(30) # in seconds
		except self.StopThread:
			pass
