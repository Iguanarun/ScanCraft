#! /usr/bin/env python3

import os,shutil,subprocess
from .operations.GetDir import GetDir
from .color_print import ColorPrint,UseStyle,Error
from .read.readSLHA import ReadSLHAFile
from .data_type import data_list
from .Experiments.dSphs.IDD import X2_dSphs
from .Experiments.GCE.testCovar import X2_GCE

class MicrOMEGAs():
    def __init__(self,
                    package_dir=None,
                    model='NMSSM',
                    main_routine='./main',
                    data_dir='mcmc/',):
        if package_dir==None:
            package_dir=GetDir('micromegas')
        elif not os.path.exists(package_dir):
            Error('=self.output_dir --%s-- not found, please check its path'%package_dir)
        
        self.package_dir=package_dir
        self.model_dir=model
        self.work_dir=os.path.join(package_dir,model)
        # self.inp_file='SPheno.spc.NInvSeesaw'#------------
        # self.inp_dir=os.path.join(self.work_dir,self.inp_file)
        self.output_file='Omega.txt'#------------
        self.output_dir=os.path.join(self.work_dir,self.output_file)
        self.record_dir=os.path.join(data_dir,'./record/')
        self.command=main_routine

    def GCE_X2(self,sample=None):
        if sample is None:
            sample=self.result
        return X2_GCE(os.path.join(self.work_dir,'EEdN_dEdO_sight.txt'),eps=sample.ABUNDANCE[4]/0.1197)

        # command=' '.join(['./testCovar.py',os.path.join(self.work_dir,'EEdN_dEdO_sight.txt')])
        # run=subprocess.Popen(command,
        #     # cwd='./command/Experiments/GCE/',
        #     cwd='/home/heyangle/Desktop/ScanCommando/ScanCommando/command/Experiments/GCE',
        #     shell=True,
        #     stdout=subprocess.PIPE)
        # run.wait()
        # return float(run.stdout.read())

    def IDD_X2(self,sample):
        return X2_dSphs(os.path.join(self.work_dir,'E_dNdE_single.txt'),
                        sample.ABUNDANCE[0],# m_DM
                        sample.ABUNDANCE[4],# Omega
                        sample.ANNIHILATION['SigmaV']# SigmaV
                        )

    def Run(self,in_file='',sample=None):
        if sample is None:  sample=data_list()
        try:delattr(self,'result')
        except:pass
        command=' '.join([self.command,in_file])
        run=subprocess.Popen(command,
            cwd=self.work_dir,shell=True,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,universal_newlines=True)
        run.wait()
        if (run.returncode):
            ColorPrint(0,33,'',run.communicate()[0])
            Error(run.communicate()[1])
        else:
            ReadSLHAFile(self.output_dir,sample=sample)
            self.result=sample
        return sample
    
    def Record(self,number,directory=None):
        if directory is None: directory=self.record_dir
        shutil.move(self.output_dir,os.path.join(directory,self.output_file+'.'+str(int(number))))