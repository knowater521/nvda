# NVDA Configuration Support

configFileName = "nvda.ini"

import os
from StringIO import StringIO
from configobj import ConfigObj
from validate import Validator
val = Validator()

### The configuration specification
confspec = StringIO("""# NVDA Configuration File

# Speech settings
[speech]
	# The synthesiser to use
	synth = string(default=sapi5)

	[[__many__]]
		rate = integer(default=60)
		pitch = integer(default=50)
		volume = integer(default=100)
		voice = integer(default=1)
		relativeUppercasePitch = integer(default=20)

# Presentation settings
[presentation]
		reportClassOfClientObjects = boolean(default=true)
		reportClassOfAllObjects = boolean(default=false)
		reportKeyboardShortcuts = boolean(default=true)
		reportTooltips = boolean(default=true)
		reportHelpBalloons = boolean(default=true)

[mouse]
	reportObjectUnderMouse = boolean(default=true)
	reportMouseShapeChanges = boolean(default=false)

[documentFormat]
	reportFontChanges = boolean(default=false)
	reportFontSizeChanges = boolean(default=true)
	reportFontAttributeChanges = boolean(default=True)
	reportAlignmentChanges = boolean(default=True)
	reportStyleChanges = boolean(default=false)
	reportTables = boolean(default=true)
	reportPageChanges = boolean(default=true)
 

""".replace("\n", "\r\n"))

### Globals
conf = None
mtime = 0

def load():
	global conf, mtime
	# If the config file exists, store its mtime.
	if os.path.isfile(configFileName):
		mtime = os.path.getmtime(configFileName)
	conf = ConfigObj(configFileName, configspec = confspec, indent_type = "\t")
	# Python converts \r\n to \n when reading files in Windows, so ConfigObj can't determine the true line ending.
	conf.newlines = "\r\n"
	conf.validate(val)
	checkSynth()

def checkSynth():
	"Validate the configuration for the selected synth."
	speech = conf["speech"]
	synth = speech["synth"]
	# If there are no settings for this synth, make sure there are defaults.
	if not speech.has_key(synth):
		speech[synth] = {}
		conf.validate(val, copy = True, section = speech)

def save(force = False):
	global conf, mtime
	# If the file has changed since it was read, don't save over the top of it.
	if not force and os.path.isfile(configFileName) and os.path.getmtime(configFileName) != mtime:
		return
	# Copy default settings and formatting.
	conf.validate(val, copy = True)
	conf.write()

def getSynthConfig():
	"A convenience function to return the config for the current speech synth."
	return conf["speech"][conf["speech"]["synth"]]

### Main
load()
