'''
Created on Jun 22, 2013

@author: mxu
'''
from ChorusCore import Utils, ExceptionManagement
from ChorusCore.APIManagement import Request
from ChorusCore.Log import Output, Formatter, Logger, Name
from ChorusCore import Log
import json, logging

class Mode:
    '''
    There are two mode of mock server which has totally different behavior:
    1. Mock: mock server will return static response predefined
    2. Proxy: mock server will forward request to real server, which serves as a proxy
    '''
    Mock = "Mock"
    Proxy = "Proxy"
    
def LoadJson(json_file, json_path = None):


    assertResult = Utils.AssertConfig("MOCK_SERVER", "JsonTemplatePath")
    paths = ['Projects']
    if assertResult:
        for path in Utils.GetConfig("MOCK_SERVER","jsontemplatepath").split("."):
            paths.append(path)
        if json_path:
            if isinstance(json_path, str):
                paths.append(json_path)
            elif isinstance(json_path, list) or isinstance(json_path, tuple):
                for jpath in json_path:
                    paths.append(jpath)
            else:
                print "unrecognized path list!"
        
    try:
        result = Utils.GetJsonFromFile(paths, json_file)
    except Exception, e:
        
        result = {"mock_server_error":"invalid json file","exception": str(e)}

    return result
def LoadImage(image_file):
    config = Utils.config
    Utils.AssertConfig("MOCK_SERVER", "JsonTemplatePath")
    paths=['Projects']
    for path in config["MOCK_SERVER"]["jsontemplatepath"].split("."):
        paths.append(path)
    try:
        f = open(Utils.GetFileStr(paths,image_file), 'rb')
        data = f.read()
    except Exception, e:
        data = {"mock_server_error":"invalid image file"}
    return data

def SetResponse(module_name, data):
    '''
    set data returned by mock server
    Two args: 
        The first arg is the module instance of the api template
        The second arg is response we'd like to set
    if success, return true. else, return false
    '''
    url, api_path = _get_baseurl()
    uri = "/set/response"    
    #assamble body
    print "test"+ url, api_path
    module = __import__('Projects.%s.%s' % (api_path, module_name),globals(),locals(),[module_name, ''],-1)     
    print 'this is module'
    print module
    body = {
            "url": module.url,
            "method": module.method,
            "response": data
            }
    print body
    try:
        request = Request(url = uri, body = body, method = "post", base_url = url)
        print request
        result = request.send().result
        print 'this is result'
        print result
        if result['status'] == '200':
            Log.Chorus.debug("Set response success!")
            return True
        else:
            Log.Chorus.debug("Set response failed!")
            return False
    except:
        Log.Chorus.exception("Error response returned!")
        return False
    
def _get_baseurl():
    section = "MOCK_SERVER"
    config = Utils.config
    Utils.AssertConfig(section, "BASEURL")
    Utils.AssertConfig(section, "Port")
    Utils.AssertConfig(section, "SSL")
    Utils.AssertConfig(section, "APITemplatePath")
    try:
        port = int(config[section]["port"])
    except:
        raise ExceptionManagement.IncorrectConfigError("Port should be an integer")
    #assamble url
    try:
        if config[section]["ssl"].lower() == "true":
            ssl = True
        else:
            ssl = False
    except:
        ssl = False
    if ssl:
        prefix="https://"
    else:
        prefix="http://"
    ip = config[section]["baseurl"]
    port = config[section]["port"]    
    url = prefix + ":".join((ip,port))    
    api_path = config[section]["apitemplatepath"]

    return url, api_path

def SetDelay(delay = 0, is_global = False):
    '''
    by default the delay is 0. set value to get a delayed response. The value must be int type.
    '''
    if not isinstance(delay, int):
        raise Log.Chorus.exception("delay must be integer!")
        
    url, api_path = _get_baseurl()
    uri = "/set/delay"     
    body = { 'delay': delay , 'is_global': is_global}
    try:
        request = Request(url = uri, body = body, method = "post", base_url = url)
        result = request.send().result
        if result['status'] == '200':
            Log.Chorus.debug("Set delay success!")
            return True
        else:
            Log.Chorus.debug("Set delay failed!")
            return False
    except:
        Log.Chorus.exception("Error response returned!")
        return False    
    


def SetMode(mode = Mode.Mock, is_global = True):
    '''
    by default set mode will change mode permenently. If you don't want this, set global to false
    '''
    url, api_path = _get_baseurl()
    uri = "/set/mode"     
    body = { 'mode': mode, 'is_global': is_global}
    try:
        request = Request(url = uri, body = body, method = "post", base_url = url)
        result = request.send().result
        if result['status'] == '200':
            Log.Chorus.debug("Set mode success!")
            return True
        else:
            Log.Chorus.debug("Set mode failed!")
            return False
    except:
        Log.Chorus.exception("Error response returned!")
        return False

if __name__ == "__main__":
    Utils.configfile = "mockserver_Demo.cfg"
    Utils.configfilePath = "Trela3_6"
    Utils.InitConfig()
    from Projects.Alert.Resource.APITemplates import giftcards_detail_error

    Log.Chorus = Logger(name = Name.ChorusCore, loglevel = logging.DEBUG, output = Output.Console, formatter = Formatter.ChorusCore).get_logger()
    print SetResponse("giftcards_detail_error", giftcards_detail_error.response_821)
#    from Projects.Usher.UVS.APITemplates import user_retrieve__events_get
#    print SetResponse("user_retrieve__events_get", user_retrieve__events_get.response_device_activation)
    #SetMode(mode = Mode.Mock, is_global = False)
    #SetDelay()