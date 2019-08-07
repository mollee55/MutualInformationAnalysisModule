# -*- coding: utf-8 -*-
import unittest
import os  # noqa: F401
import json  # noqa: F401
import time
import requests

from os import environ
try:
    from ConfigParser import ConfigParser  # py2
except:
    from configparser import ConfigParser  # py3

from pprint import pprint  # noqa: F401

from biokbase.workspace.client import Workspace as workspaceService
from MutualInformationAnalysisModule.MutualInformationAnalysisModuleImpl import MutualInformationAnalysisModule
from MutualInformationAnalysisModule.MutualInformationAnalysisModuleServer import MethodContext
from MutualInformationAnalysisModule.authclient import KBaseAuth as _KBaseAuth


class MutualInformationAnalysisModuleTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        cls.cfg = {}
        config = ConfigParser()
        config.read(config_file)
        for nameval in config.items('MutualInformationAnalysisModule'):
            cls.cfg[nameval[0]] = nameval[1]
        # Getting username from Auth profile for token
        authServiceUrl = cls.cfg['auth-service-url']
        auth_client = _KBaseAuth(authServiceUrl)
        user_id = auth_client.get_user(token)
        # WARNING: don't call any logging methods on the context object,
        # it'll result in a NoneType error
        cls.ctx = MethodContext(None)
        cls.ctx.update({'token': token,
                        'user_id': user_id,
                        'provenance': [
                            {'service': 'MutualInformationAnalysisModule',
                             'method': 'please_never_use_it_in_production',
                             'method_params': []
                             }],
                        'authenticated': 1})
        cls.wsURL = cls.cfg['workspace-url']
        cls.wsClient = workspaceService(cls.wsURL)
        cls.serviceImpl = MutualInformationAnalysisModule(cls.cfg)
        cls.scratch = cls.cfg['scratch']
        cls.callback_url = os.environ['SDK_CALLBACK_URL']

    @classmethod
    def tearDownClass(cls):
        if hasattr(cls, 'wsName'):
            cls.wsClient.delete_workspace({'workspace': cls.wsName})
            print('Test workspace was deleted')

    def getWsClient(self):
        return self.__class__.wsClient

    def getWsName(self):
        if hasattr(self.__class__, 'wsName'):
            return self.__class__.wsName
        suffix = int(time.time() * 1000)
        wsName = "test_MutualInformationAnalysisModule_" + str(suffix)
        ret = self.getWsClient().create_workspace({'workspace': wsName})  # noqa
        self.__class__.wsName = wsName
        return wsName

    def getImpl(self):
        return self.__class__.serviceImpl

    def getContext(self):
        return self.__class__.ctx

    # NOTE: According to Python unittest naming rules test method names should start from 'test'. # noqa
    def test_your_method(self):
        # Prepare test objects in workspace if needed using
        # self.getWsClient().save_objects({'workspace': self.getWsName(),
        #                                  'objects': []})
        #
        # Run your method by
        # ret = self.getImpl().your_method(self.getContext(), parameters...)
        #
        # Check returned data with
        # self.assertEqual(ret[...], ...) or other unittest methods

        params = {'fbamodel_id': "iML1515.kb", 'compounds': 'cpd00001_c0,cpd00001_e0,cpd00007_c0,cpd00027_c0',
                 'media_id': "Carbon-D-Glucose-iML1515", 'workspace_name': 'filipeliu:narrative_1564175222344','mi_options': 'secretion'}

        #params = {'fbamodel_id': "Pseudomonas_fluorescens_SBW25.RAST", 'compounds': 'cpd00001_c0,cpd00001_e0,cpd00002_c0,cpd00003_c0',
        #        'media_id': "Carbon-D-Glucose", 'workspace_name': 'zahmeeth:narrative_1537200416208','mi_options': 'flux'}

        #params = {'fbamodel_id': "meh", 'compounds': "foo", 'media_id': "bar", 'workspace_name': self.getWsName()}

        print('test methd!')
        self.getImpl().run_flux_mutual_information_analysis(self.ctx, params)

        """
        file_ref = "5068/44/2"
        data = self.getWsClient().get_objects([{"ref": file_ref}])[0][
            "data"]

        with open(self.scratch + "/output.txt", "w+") as outfile:
            json.dump(data, outfile)
        
        """
