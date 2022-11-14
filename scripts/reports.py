#!/usr/bin/env python3

## Access to lab work
# chmod 600 ~/Downloads/qwiklabs-L35392721.pem
# ssh -i ~/Downloads/qwiklabs-L35392721.pem student-00-eaaf4890807f@35.194.27.236
# pip install reportlab
# pip install pandas
# MgRbQ3QMiuQx

## Run to correct work
# pip install reportlab
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Paragraph, Spacer, Table, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

def generate(filename, title, additional_info, table_data):
  styles = getSampleStyleSheet()
  report = SimpleDocTemplate(filename)
  report_title = Paragraph(title, styles["h1"])
  report_info = Paragraph(additional_info, styles["BodyText"])
  table_style = [('GRID', (0,0), (-1,-1), 1, colors.black),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('ALIGN', (0,0), (-1,-1), 'CENTER')]
  report_table = Table(data=table_data, style=table_style, hAlign="LEFT")
  empty_line = Spacer(1,20)
  report.build([report_title, empty_line, report_info, empty_line, report_table])

