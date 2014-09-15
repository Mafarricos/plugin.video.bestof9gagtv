#!/usr/bin/python
# -*- coding: utf-8 -*-

import urllib
import urllib2
import json
import socket
import xbmcaddon
import xbmcplugin
import xbmcgui
import sys
import re

addon = xbmcaddon.Addon()
socket.setdefaulttimeout(30)
pluginhandle = int(sys.argv[1])
addonID = addon.getAddonInfo('id')
xbox = xbmc.getCondVisibility("System.Platform.xbox")
translation = addon.getLocalizedString
icon = xbmc.translatePath('special://home/addons/'+addonID+'/icon.png')
urlMain = "http://9gag.tv/api/index/nJ1gX?ref_key=&count=20&direction=1&includeSelf=0"

def index():
    addDir(translation(30001), urlMain, "listVideos", icon)
    xbmcplugin.endOfDirectory(pluginhandle)

def playVideo(id):
    if xbox:
        url = "plugin://video/YouTube/?path=/root/video&action=play_video&videoid=" + id
    else:
        url = "plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=" + id
    listitem = xbmcgui.ListItem(path=url)
    xbmcplugin.setResolvedUrl(pluginhandle, True, listitem)


def listVideos(url):
    content = getUrl(url)
    content_json = json.loads(content)
    nbEntries = len(content_json['data']['posts'])
    for i in range(0, nbEntries-1, 1):
        title = content_json['data']['posts'][i]['title']
        id = content_json['data']['posts'][i]['videoCover']['videoExternalId']
        thumb = content_json['data']['posts'][i]['thumbnail_120w']
        description = content_json['data']['posts'][i]['ogDescription']
        addLink(title, id, "playVideo", thumb, description)
    xbmcplugin.endOfDirectory(pluginhandle)


def getUrl(url):
    req = urllib2.Request(url)
    req.add_header('User-Agent', 'BestOf9GagTV XBMC Addon v0.1.0')
    response = urllib2.urlopen(req)
    content = response.read()
    response.close()
    return content

def addLink(name, url, mode, iconimage, desc):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultVideo.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": desc})
    liz.setProperty('IsPlayable', 'true')
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz)
    return ok


def addDir(name, url, mode, iconimage):
    u = sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def parameters_string_to_dict(parameters):
    ''' Convert parameters encoded in a URL to a dict. '''
    paramDict = {}
    if parameters:
        paramPairs = parameters[1:].split("&")
        for paramsPair in paramPairs:
            paramSplits = paramsPair.split('=')
            if (len(paramSplits)) == 2:
                paramDict[paramSplits[0]] = paramSplits[1]
    return paramDict

params = parameters_string_to_dict(sys.argv[2])
mode = urllib.unquote_plus(params.get('mode', ''))
url = urllib.unquote_plus(params.get('url', ''))

if mode == 'listVideos':
    listVideos(url)
elif mode == 'playVideo':
    playVideo(url)
else:
    index()
