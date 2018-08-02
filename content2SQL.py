# -*- coding: utf-8 -*-
"""
Created on Mon Feb 26 18:51:53 2018

@author: Rui Wenhao
@Copyright: Rui Wenhao, All rights reserved
@Mail:rui_wenhao@cueb.edu.cn
"""

import MySQLdb

class mySql:
    
    def __init__(self,host,port,db,user,passwd,charset='utf8'):
        self.host=host
        self.port=port
        self.db=db
        self.user=user
        self.passwd=passwd
        self.charset=charset

    def connect(self):
        self.conn=MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,db=self.db,charset=self.charset)
        self.cursor=self.conn.cursor()
        
    def close(self):
        self.cursor.close()
        self.conn.close()
        
    def create_table(self,table_name):
        try:
            self.connect()
            self.q = 'create table %s '\
                '(source CHAR(15),keyword CHAR(15),links VARCHAR(500),city CHAR(20),'\
                'company CHAR(50),position VARCHAR(50),education CHAR(20),salary CHAR(30),'\
                'description TEXT,experience CHAR(30),scale CHAR(30),categoty CHAR(30))' % table_name
            
            self.cursor.execute(self.q)
            self.close()
        except MySQLdb.Error as e:
            print(e)
        
    def innsert_data(self,line,table_name):
        try:
            self.connect()
            self.cursor.execute('insert into %s values %s' % (table_name,tuple(line.values())))
            self.conn.commit()
            self.close()
        except MySQLdb.Error as e:
            print(e)

    
        
        
