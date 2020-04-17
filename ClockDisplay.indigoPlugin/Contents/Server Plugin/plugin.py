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

from datetime import timedelta

from sunrise_sunset import SunriseSunset

# Note the "indigo" module is automatically imported and made available inside
# our global name space by the host process.

################################################################################
class Plugin(indigo.PluginBase):
	########################################
	def __init__(self, pluginId, pluginDisplayName, pluginVersion, pluginPrefs):
		super(Plugin, self).__init__(pluginId, pluginDisplayName, pluginVersion, pluginPrefs)
		self.dTimeDelta = -1576800000  #-10
		self.dTime = time.time()
		self.sleepTime = 30
		self.dontStart = True
		
		
		
		indigo.server.log("Waiting for system clock to reach :00 seconds...")

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
		latLong=indigo.server.getLatitudeAndLongitude()
		self.myLat = latLong[0]
		self.myLong = latLong[1]
		self.tzOffset = int(time.strftime("%z")) / 100
		ro = SunriseSunset(datetime.datetime.now(), latitude=self.myLat,longitude=self.myLong, localOffset=self.tzOffset)
		self.rise_time, self.set_time = ro.calculate()
		
		self.rise_time = self.rise_time.strftime(dev.ownerProps.get("risesetformat","%H:%M"))
		self.set_time = self.set_time.strftime(dev.ownerProps.get("risesetformat","%H:%M"))
		
		#self.set_time.strftime(dev.ownerProps.get("risesetformat","%H:%M"))
		#indigo.server.log(str(self.set_time))
		#indigo.server.log(str(self.set_time.strftime(dev.ownerProps.get("risesetformat","%H:%M"))))

	def runConcurrentThread(self):
		try:
			while True:
			
				if (self.dontStart):
					secs = time.strftime("%S")
					#indigo.server.log(secs)
					if (int(secs) > 1):
						self.sleep(1)
						continue
					else:
						indigo.server.log("Starting clock timer at {} seconds".format(secs))
						self.dontStart = False
			
				for d in indigo.devices.iter("self.clockdisplay"):
					self.tzOffset = int(time.strftime("%z")) / 100 #Get timezone in case it changed this morning
					if ((self.tzOffset != d.states["TZ_Offset"]) or (time.strftime("%d/%m/%y") != d.states["DateUK_DDMMYY"])):
						#indigo.server.log("New Day")
						
						ro = SunriseSunset(datetime.datetime.now(), latitude=self.myLat,longitude=self.myLong, localOffset=self.tzOffset)
						self.rise_time, self.set_time = ro.calculate()
						
						self.rise_time = self.rise_time.strftime(d.ownerProps.get("risesetformat","%H:%M"))
						self.set_time = self.set_time.strftime(d.ownerProps.get("risesetformat","%H:%M"))
					minOfDay = (int(time.strftime("%H")) * 60)+int(time.strftime("%M"))
					#indigo.server.log(str(minOfDay))
					key_value_list = [
					{"key":"DateUK_DDMMYY","value":time.strftime("%d/%m/%y")},
					{"key":"DateUK_DDMMYYYY","value":time.strftime("%d/%m/%Y")},
					{"key":"DateUS_MMDDYY","value":time.strftime("%m/%d/%y")},
					{"key":"DateUS_MMDDYYYY","value":time.strftime("%m/%d/%Y")},
					{"key":"Day_Long","value":time.strftime("%A")},
					{"key":"Day_Short","value":time.strftime("%a")},
					{"key":"LocalDate","value":time.strftime("%x")},
					{"key":"Time_12HHMM","value":time.strftime("%I:%M")},
					{"key":"Time_12HHMMSS","value":time.strftime("%I:%M:%S")},
					{"key":"Time_24HHMM","value":time.strftime("%H:%M")},
					{"key":"Time_24HHMMSS","value":time.strftime("%H:%M:%S")},
					{"key":"Time_12HHMMAMPM","value":time.strftime("%I:%M%p")},
					{"key":"Time_12HHMMSSAMPM","value":time.strftime("%I:%M:%S%p")},
					{"key":"Time_24HHMMAMPM","value":time.strftime("%H:%M%p")},
					{"key":"Time_24HHMMSSAMPM","value":time.strftime("%H:%M:%S%p")},
					{"key":"Time_12HHMMAMPML","value":time.strftime("%I:%M%p").lower()},
					{"key":"Time_12HHMMSSAMPML","value":time.strftime("%I:%M:%S%p").lower()},
					{"key":"Time_24HHMMAMPML","value":time.strftime("%H:%M%p").lower()},
					{"key":"Time_24HHMMSSAMPML","value":time.strftime("%H:%M%p").lower()},
					{"key":"Time_12HMM","value":time.strftime("%-I:%M")},
					{"key":"Time_12HMMSS","value":time.strftime("%-I:%M:%S")},
					{"key":"Time_24HMM","value":time.strftime("%-H:%M")},
					{"key":"Time_24HMMSS","value":time.strftime("%-H:%M:%S")},
					{"key":"Time_12HMMAMPM","value":time.strftime("%-I:%M%p")},
					{"key":"Time_12HMMSSAMPM","value":time.strftime("%-I:%M:%S%p")},
					{"key":"Time_24HMMAMPM","value":time.strftime("%-H:%M%p")},
					{"key":"Time_24HMMSSAMPM","value":time.strftime("%-H:%M:%S%p")},
					{"key":"Time_12HMMAMPML","value":time.strftime("%-I:%M%p").lower()},
					{"key":"Time_12HMMSSAMPML","value":time.strftime("%-I:%M:%S%p").lower()},
					{"key":"Time_24HMMAMPML","value":time.strftime("%-H:%M%p").lower()},
					{"key":"Time_24HMMSSAMPML","value":time.strftime("%-H:%M%p").lower()},
					{"key":"LocalTime","value":time.strftime("%X")},
					{"key":"Sunrise","value":self.rise_time},
					{"key":"Sunset","value":self.set_time},
					{"key":"TZ_Offset","value":self.tzOffset},
					{"key":"MinuteOfDay","value":str(minOfDay)},
					{"key":"Custom1","value":time.strftime(d.ownerProps.get("custom1",""))},
					{"key":"Custom2","value":time.strftime(d.ownerProps.get("custom2",""))},
					{"key":"Custom3","value":time.strftime(d.ownerProps.get("custom3",""))},
					{"key":"Custom4","value":time.strftime(d.ownerProps.get("custom4",""))},
					{"key":"Custom5","value":time.strftime(d.ownerProps.get("custom5",""))},
					{"key":"Custom1L","value":time.strftime(d.ownerProps.get("custom1","")).lower()},
					{"key":"Custom2L","value":time.strftime(d.ownerProps.get("custom2","")).lower()},
					{"key":"Custom3L","value":time.strftime(d.ownerProps.get("custom3","")).lower()},
					{"key":"Custom4L","value":time.strftime(d.ownerProps.get("custom4","")).lower()},
					{"key":"Custom5L","value":time.strftime(d.ownerProps.get("custom5","")).lower()},
					]
					d.updateStatesOnServer(key_value_list)
		
					if (d.ownerProps.get("useSeconds",False)): #True
						self.sleepTime = 1
				
				self.sleep(self.sleepTime)
		except self.StopThread:
			pass
