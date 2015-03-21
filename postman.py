import csv
from jinja2 import Template
from jinja2 import Environment, meta
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import argparse
import json
class bostman:

    def getTemplate(self,template_name):
        with open(template_name) as f:
            t=Template(f.read())
            return t
    def getTemplateVars(self,template_name):
        env = Environment()
        with open(template_name) as f:
            ast = env.parse(f.read())
        s=meta.find_undeclared_variables(ast)
        print list(s)


    def read_mail_list(self,csv_file):
        reader = csv.DictReader(open(csv_file))
        return reader

    def parse_config(self):
        with open('config.json') as data_file:    
            data = json.load(data_file)
        return data
    def send_mail(self,name,to,subject,message):
        msg = MIMEMultipart('alternative')
        msg['subject']=subject
        msg['to']=to
        msg['from']=self.parse_config()['login']
        part1 = MIMEText('nothing', 'plain')
        part2 = MIMEText(message, 'html')
        msg.attach(part1)
        msg.attach(part2)
        server = smtplib.SMTP(self.parse_config()['server']+":"+self.parse_config()['port'])
        server.starttls()
        server.login(self.parse_config()['login'],self.parse_config()['password'])
        server.sendmail(name, to, msg.as_string())
        server.quit()
    def main(self):
        parser = argparse.ArgumentParser(usage="-h for full usage")
        parser.add_argument('-t', dest="template", help='email template',required=True)
        parser.add_argument('-c', dest="csv", help='list of emails',required=True)
        parser.add_argument('-subject', dest="subject", help='email subject',required=True)
        args = parser.parse_args()
        template=self.getTemplate(args.template)
        for line in self.read_mail_list(args.csv):
            message=template.render(name=line['name'])
            self.send_mail('walid',line['email'],args.subject,message)
            print 'Email sent to %s' % line['name']
        #getTemplateVars('templates/template.html')

if __name__ == '__main__':
    bostman().main()