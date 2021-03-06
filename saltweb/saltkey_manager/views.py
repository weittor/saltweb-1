#coding: utf-8

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import render_to_response
from saltweb.api import *
import re

@require_login
def accepted_list(request):
	username,role_name,usergroup_name = get_session_user(request)
	session_role_id = request.session['role_id']
	nav = perm_nav(request)
	search = request.GET.get('search','')
	if search:
		accepted_key = []
		accepted_key_list = SALTAPI.list_all_key()['return'][0]['data']['return']['minions']
		for key in accepted_key_list:
			match = re.search(search,key)
			if match:
				accepted_key.append(match.group())
		print accepted_key
	else:
		accepted_key = SALTAPI.list_all_key()['return'][0]['data']['return']['minions']
        '''分页'''
        try:
                page = int(request.GET.get('page','1'))
        except ValueError:
                page = 1
        pagenum = 10
        p = paging(page,pagenum,accepted_key)
        pt = p.pt()
        ppn = p.ppn()
        npn = p.npn()
        pn = p.pn()
        pl = p.pl()
        if page < 9:
                pr = p.pr()[0:9]
        elif int(pn) - page < 9:
                pr = p.pr()[int(pn)-9:int(pn)]
        else:
                pr = p.pr()[page-9:page+8]
	return render_to_response('saltkey_manager/accepted_list.html',locals())

@require_login
def unaccepted_list(request):
        username,role_name,usergroup_name = get_session_user(request)
	session_role_id = request.session['role_id']
	nav = perm_nav(request)
        unaccepted_key = SALTAPI.list_all_key()['return'][0]['data']['return']['minions_pre']
        '''分页'''
        try:
                page = int(request.GET.get('page','1'))
        except ValueError:
                page = 1
        pagenum = 10
        p = paging(page,pagenum,unaccepted_key)
        pt = p.pt()
        ppn = p.ppn()
        npn = p.npn()
        pn = p.pn()
        pl = p.pl()
        if page < 9:
                pr = p.pr()[0:9]
        elif int(pn) - page < 9:
                pr = p.pr()[int(pn)-9:int(pn)]
        else:
                pr = p.pr()[page-9:page+8]
	return render_to_response('saltkey_manager/unaccepted_list.html',locals())

@require_super_user
def accept_key_ajax(request):
	saltkey = request.POST.get('saltkey')
	try:
		SALTAPI.accept_key(saltkey)
		ret = u'key: %s 认证成功' %saltkey
        except Exception as e:
                ret = u'key: %s 认证失败: %s' %(saltkey,e)
        return HttpResponse(ret)

@require_super_user
def delete_key_ajax(request):
	saltkey = request.POST.get('saltkey')
        try:
                SALTAPI.delete_key(saltkey)
                ret = u'key: %s 删除成功' %saltkey
        except Exception as e:
                ret = u'key: %s 删除失败: %s' %(saltkey,e)
        return HttpResponse(ret)
