#!/usr/bin/python

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from docopt import docopt


__doc__ = """Usage:
	%(name)s set OUTLET STATE
	%(name)s get [OUTLET]
	%(name)s tgl OUTLET
	%(name)s ccl OUTLET [--delay=SEC]
	%(name)s rename OUTLET NAME
	%(name)s reset OUTLET
	%(name)s -h | --help | --version

The most commonly used commands are:
	set			Set the outlet to a given state
	get			Get the name and state of the outlets
	tgl			Toggle the state of an outlet
	ccl			Power cycle a given outlet
	reset			Rename an outlet to a default value
	rename			Rename a given outlet.
				If outlet is 'ctrl' this will rename the PowerSwitch

Arguments:
	OUTLET			outlet number (or name) to be controlled
	STATE			can be on, off, ccl

Options:
	--version		show version and exit
	-h, --help		show this help message and exit
	-v, --verbose		print status messages
	--delay			set number of seconds when power cycling


""" % {'name': os.path.basename(__file__)}


class PowerSwitchException(Exception):
	pass

class PowerSwitch:
	def __init__(self, config):
		if not os.path.exists(config):
			#so lets create the file
			print "Generating configuration file..."
			ip     = raw_input("IP address [192.168.0.100] : ") or "192.168.0.100"
			user   = raw_input("username [admin] : ") or "admin"
			passwd = raw_input("password [] : ") or ""

			f = open(config, 'w')
			f.write("# This file is used by the pw command to control a web power switch\n")
			f.write("USER=\"" + user + "\"\n")
			f.write("PASSWORD=\"" + passwd + "\"\n")
			f.write("POWER_SWITCH_IP=\"" + ip + "\"\n")
			f.close()

		# self.configuration contains all what is defiled in the config file
		self.configuration = self.parse_config(config)
		self.url = "http://" + str(self.configuration['POWER_SWITCH_IP'])
		self.timeout = (1, 3)
		# self.delay contains delay settings for each outlet
		self.delay = []

		self._get_pw(self.url + "/index.htm", None)

		self.name = self.get_switch_name()
		self.outlets = self.get_outlets_state()




	def _get_pw(self, page, payload):
		try:
			ret = requests.get(page, timeout=self.timeout, params=payload,
					auth=(self.configuration['USER'], self.configuration['PASSWORD']))
		except (requests.exceptions.ReadTimeout,
				requests.exceptions.ConnectTimeout) as e :
			raise PowerSwitchException(" ERROR: Connection timed out")
		except requests.exceptions.ConnectionError as e :
			raise PowerSwitchException(" ERROR: could not reach the PowerSwitch ")

		return ret




	def _check_outlet(self, outlet):
		if str(outlet) not in "all 1 2 3 4 5 6 7 8":
			print " ERROR: Asking for an outlet out of range !"
			sys.exit(1)




	def parse_config(self, filename):
		options = {}
		f = open(filename)
		for line in f:
			# First, remove comments:
			if '#' in line:
				# split on comment char, keep only the part before
				line, comment = line.split('#', 1)
				# Second, find lines with an option=value:
			if '=' in line:
				# split on option char:
				option, value = line.split('=', 1)
				# strip spaces quotes and newline
				option = option.strip()
				value = value.strip(" \"\n")
				# store in dictionary:
				options[option] = value
		f.close()
		return options




	def get_switch_revision(self):
		r = self._get_pw(self.url + "/support.htm", None)

		soup = BeautifulSoup(r.text, 'html.parser')

		ret = {}
		# FIXME: This is based on the assumption that the different
		# fields do not change order in other revisions..
		table_lines = soup.findAll('td', width="70%")
		ret['firmware']  = table_lines[0].string.strip()
		ret['hardware']  = table_lines[1].string.strip()
		ret['serialnum'] = table_lines[3].string.strip()

		return ret




	def get_switch_name(self):
		r = self._get_pw(self.url + "/index.htm", None)
		soup = BeautifulSoup(r.text, 'html.parser')

		return soup.findAll('th', bgcolor="#DDDDFF")[0].string.strip()




	def get_outlets_state(self):
		r = self._get_pw(self.url + "/index.htm", None)
		soup = BeautifulSoup(r.text, 'html.parser')

		ret = []
		for table_line in soup.findAll('tr', bgcolor="#F4F4F4"):
			outlet = {}
			index = int(table_line.findAll('td')[0].string)
			# Add other outlet specifics here
			outlet["index"] = str(index)
			outlet["name"]  = str(table_line.findAll('td')[1].string)
			outlet["state"]  = str(table_line.findAll('font')[0].string)
			ret.append(outlet)

		return ret




	def print_outlet_state(self, outlet=None):

		self.get_outlets_state()
		print self.name
		if outlet is None:
			for outlet in self.outlets:
				name= "  " + outlet['name'] + " "
				print name.ljust(25, '.'), outlet['index'], " - ", outlet['state']
		else:
			self._check_outlet(outlet)
			outlet = self.outlets[int(outlet) - 1]

			name= "  " + outlet['name'] + " "
			print name.ljust(25, '.'), outlet['index'], " - ", outlet['state']




	def set_outlet_state(self, outlet, state):

		self._check_outlet(outlet)
		if state in "on off ccl":
			payload = { outlet: state.upper()}
		else:
			print " ERROR: \"" + state + "\" is not a valid state."
			sys.exit(1)

		self._get_pw(self.url + "/outlet", payload)




	def toggle_outlet(self, outlet):

		self._check_outlet(outlet)
		if self.outlets[int(outlet)-1]['state'] == "OFF":
			self.set_outlet_state(outlet, "on")
		else:
			self.set_outlet_state(outlet, "off")



	def set_name(self, outlet, name):

		if outlet == 'ctrl':
			payload = { 'ctrlname': name}

		else:
			self._check_outlet(outlet)

			for out in self.outlets:
				if name == out['name']:
					print " ERROR: name already used by outlet " + out['index']
					sys.exit(1)

			payload = { 'outname'+str(outlet): name}

		self._get_pw(self.url + "/unitnames.cgi?data", payload)




	def reset_outlet_name(self, outlet=None):

		if outlet is None:
			for i in self.outlets:
				self.set_name(i['index'], "Outlet "+str(i['index']))
		else:
				self.set_name(outlet, "Outlet "+str(outlet))




	def get_delay_settings(self):
		r = self._get_pw(self.url + "/admin.htm", None)
		soup = BeautifulSoup(r.text, 'html.parser')

		for i in range(9, 13):
			tmp = soup.findAll('tr', bgcolor="#F4F4F4")[i]
			delay = {}
			delay[tmp.findAll('td')[0].string.replace(' ', '_')] = tmp.findAll('td')[1].find('input').get('value')
			self.delay.append(delay)




	#TODO
	#def set_delay_settings(self):
	#def get_network_settings(self):
	#def set_network_settings(self):




if __name__ == "__main__":

	arguments = docopt(__doc__)

	conffile=os.path.expanduser("~/." + os.path.basename(__file__) + ".conf")
	try:
		pw = PowerSwitch(conffile)

		if arguments['--version']:
			rev = pw.get_switch_revision()
			print "PW\t\tpy-1.0"
			for k,v in rev.items():
				print k.upper(), '\t', v

		# first lets check if you're trying to access by name
		# if we are, get index matching name
		for out in pw.outlets:
			if out['name'] == arguments['OUTLET']:
				outlet = out['index']
				break
			else:
				outlet = None
		if outlet is None:
			outlet = arguments['OUTLET']

		if arguments['ccl']:
			if arguments['--delay'] is None:
				pw.set_outlet_state(outlet, "ccl")
			else:
				pw.set_outlet_state(outlet, "off")
				time.sleep(int(arguments['--delay']))
				pw.set_outlet_state(outlet, "on")

		if arguments['tgl']:
			pw.toggle_outlet(outlet)

		if arguments['get']:
			pw.print_outlet_state(outlet)

		if arguments['set']:
			pw.set_outlet_state(outlet, arguments['STATE'])

		if arguments['rename']:
			pw.set_name(outlet, arguments['NAME'])

		if arguments['reset']:
			pw.reset_outlet_name(outlet)

	except PowerSwitchException as e:
		print "FOO ", e



# vim: set ft=python cc=80: