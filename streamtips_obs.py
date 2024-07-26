import time, random, re, json
from string import Formatter
from os import path
#open("streamloading.json",mode="r",encoding="utf-8")
strgroup = None
loadarray = ["ERROR"]
tiparray = ["ERROR"]
changetip = 0
dictionary_keyword = re.compile("\\{.*?\\}")

import obspython as obs

loading_source_name = ""
tip_source_name = ""
cycleratemin = 1000
cycleratemax = 10000
tipchangemin = 3
tipchangemax = 10
changeenabled = False

# ------------------------------------------------------------


def blink():
    global loading_source_name, tip_source_name, changetip, cycleratemin, cycleratemax, tipchangemin, tipchangemax, changeenabled
    
    changetip -= 1
    if changeenabled:
        source1 = obs.obs_get_source_by_name(loading_source_name)
        if source1 is not None:
            changetext(source1, dictionarylookup(random.choice(loadarray)))
        obs.obs_source_release(source1)
        
        if changetip <= 0:
            source2 = obs.obs_get_source_by_name(tip_source_name)
            if source2 is not None:
                changetext(source2, "Tip: " + dictionarylookup(random.choice(tiparray)))
            obs.obs_source_release(source2)
            lmin = tipchangemin
            lmax = tipchangemax
            if lmin==lmax:
                lmax = lmin + 1
            changetip = random.randrange(min(lmin, lmax),max(lmin,lmax))
    
    obs.remove_current_callback()
    lmin = cycleratemin
    lmax = cycleratemax
    if lmin==lmax:
        lmax = lmin + 1
    obs.timer_add(blink, random.randrange(min(lmin, lmax),max(lmin,lmax)))

def changetext(source, text):
    settings = obs.obs_source_get_settings(source)
    obs.obs_data_set_string(settings, "text", text)
    obs.obs_source_update(source, settings)
    obs.obs_data_release(settings)
# ------------------------------------------------------------

def cyclebutton(properties, button):
    obs.timer_remove(blink)
    blink()
    print("pressed cycle button")
    #return True

def script_properties():
    """
    Called to define user properties associated with the script. These
    properties are used to define how to show settings properties to a user.
    """
    props = obs.obs_properties_create()
    obs.obs_properties_add_path(props, "jsonfile", "Dictionary File (.json)", obs.OBS_PATH_FILE, "JSON file (*.json)", None)
    p2 = obs.obs_properties_add_list(props, "sourceloading", "Text Source (Loading)",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    p3 = obs.obs_properties_add_list(props, "sourcetips", "Text Source (Tips)",
                                    obs.OBS_COMBO_TYPE_EDITABLE,
                                    obs.OBS_COMBO_FORMAT_STRING)
    
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_id(source)
            if source_id == "text_gdiplus" or source_id == "text_ft2_source":
                name = obs.obs_source_get_name(source)
                obs.obs_property_list_add_string(p2, name, name)
                obs.obs_property_list_add_string(p3, name, name)

        obs.source_list_release(sources)
    
    grp1 = obs.obs_properties_create()
    obs.obs_properties_add_int(grp1, "cycleratemin", "Min", 1, 10000, 1)
    obs.obs_properties_add_int(grp1, "cycleratemax", "Max", 1, 10000, 1)
    obs.obs_properties_add_group(props,"cyclerate","Cycle Rate (ms)",obs.OBS_GROUP_NORMAL,grp1)
    grp2 = obs.obs_properties_create()
    obs.obs_properties_add_int(grp2, "tipchangemin", "Min", 1, 10, 1)
    obs.obs_properties_add_int(grp2, "tipchangemax", "Max", 1, 10, 1)
    obs.obs_properties_add_group(props,"tipchange","Tip Change Rate (number of changes)",obs.OBS_GROUP_NORMAL,grp2)
    
    obs.obs_properties_add_bool(props,"enabled","Enabled")
    return props


def script_update(settings):
    """
    Called when the script’s settings (if any) have been changed by the user.
    """
    global loading_source_name
    global tip_source_name
    global strgroup
    global loadarray, tiparray, cycleratemin, cycleratemax, tipchangemin, tipchangemax, changeenabled
    
    jsonpath = obs.obs_data_get_string(settings, "jsonfile")
    if path.exists(jsonpath):
        infile = open(jsonpath,mode="r",encoding="utf-8")
        strgroup = json.load(infile)
        loadarray = strgroup.get("Loading",["ERROR"])
        tiparray = strgroup.get("Tips",["ERROR"])
    else:
        strgroup = None
    
    loading_source_name = obs.obs_data_get_string(settings, "sourceloading")
    tip_source_name = obs.obs_data_get_string(settings, "sourcetips")
    cycleratemin = obs.obs_data_get_int(settings, "cycleratemin")
    cycleratemax = obs.obs_data_get_int(settings, "cycleratemax")
    tipchangemin = obs.obs_data_get_int(settings, "tipchangemin")
    tipchangemax = obs.obs_data_get_int(settings, "tipchangemax")
    changeenabled = obs.obs_data_get_bool(settings, "enabled")
    print("changeenabled was set to " + str(changeenabled))
    
    obs.timer_remove(blink)
    obs.timer_add(blink, cycleratemin)

def dictionarylookup(istr):
    while "{" in istr:
        keywords = [fname for _, fname, _, _ in Formatter().parse(istr) if fname]
        if len(keywords) == 0:
            return istr
        for keyword in keywords:
            arg = random.choice(strgroup.get(keyword,["ERROR"]))
            istr = istr.replace("{"+keyword+"}",arg)
            #print("Replaced keyword {0} with {1}".format(keyword,arg))
            
    return istr