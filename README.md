# Standby Screen Tip Rotator Script
This is the open-source code of CAI-TAn's Standby Screen Python script for OBS, as well as a somewhat live-updating version of her streamloading.json for you to peruse at your own leisure.
## Contents
- **README.md:** That's what you're looking at right now!
- **streamloading2.json:** This is the current JSON file being used on CAI-TAn's streams.
- **streamloading.json:** Legacy uncategorized version of CAI-TAn's old JSON file. This won't get updated for a while, but it's useful as a base for your own JSON if you want.
- **streamtips_obs.py:** This is the script that can be inserted into OBS to get the same functionality from CAI-TAn's standby screen.
- **streamtips_txt.py:** An older, alternate version of the script that's based on writing to TXT files instead of working as a script within OBS.
- **.gitignore:** SCP-055 is a "self-keeping secret" or "anti-meme". Information about SCP-055's physical appearance as well as its nature, behavior, and origins is self-classifying. *I think OBS likes making .pyc files in the same folder as the script for some reason??*
## How to Use
### Installation
1. First, download the script, using any of these methods:
   - On the main page of GitHub, Click Code -> Download ZIP, then extract it to somewhere on your computer
   - Copy the code from streamtips_obs.py to a new Python .py file
   - Fork the repository for yourself
2. Create or edit a .json file containing at least one tip and at least one loading phrase. For example, here's the bare minimum:
```
{
  "Loading":
  [
    "Loading..."
  ],
  "Tips":
  [
    "This is a tip."
  ]
}
```
3. Save your .json file somewhere you can find later.
4. Add the script to OBS:
   - In the top menu bar, go to Tools -> Scripts.
   - Click the + at the bottom.
   - Locate streamtips_obs.py and open it.
5. Configure the script:
   - Make sure to add 2 Text (GDI) sources to your current OBS scene, one for the loading and one for the tips. 
     - Give them descriptive and differing names, otherwise the next steps will suck a lot.
     - If you only want the tips to show up, you can just keep the loading one hidden.
   - For Dictionary File, browse for the .json file you created / edited in step 2.
   - For Text Source (Loading), click the dropdown and find the name of the source that you want the "Loading..." text to show up in.
   - For Text Source (Tips), do the same thing but for the "Tip: This is a tip." text.
   - Configure the change rates:
     - For Cycle Rate, put a minimum of 2000 and a maximum of 5000.
     - For Tip Change Rate, put a minimum of 3 and a maximum of 6.
     - You can play with these later, but for now, these are the recommended values that I use on my stream.
6. Click the Reload Scripts button at the bottom of the script list.
   - If stuff still isn't working, first check the Script Log for any errors, then try restarting OBS.
### Keyword System
When you put curly brackets around a word, like `{STUFF}`, the code will try to replace that part of the message with a random entry from the JSON under the category of the same name. For example:
```
"Loading":
[
  "Loading {THING}..."
]
"THING":
[
  "something",
  "nothing",
  "anything"
]
```
This can result in the following examples:
> - Loading something...
> - Loading nothing...
> - Loading anything...

This system is recursive, meaning you can do something like this:
```
"Loading":
[
  "Loading {THING}..."
]
"THING":
[
  "something",
  "nothing",
  "anything",
  "{SPECIFIC}"
],
"SPECIFIC":
[
  "a game",
  "this gun",
  "deez nuts"
]
```
However, keep in mind that this does not affect the random choice distribution of {THING}, meaning that the three entries in {SPECIFIC} will have drastically less chance of showing up than the other three entries.