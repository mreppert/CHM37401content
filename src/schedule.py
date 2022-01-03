from IPython.display import display_markdown
from datetime import date
import datetime

class schedule:
    def __init__(self, meetdays, start_date):
        self.events = []
        self.start_date = date.fromisoformat(start_date)
        self.last_date = self.start_date + datetime.timedelta(-1)
        self.holidays = []
        daycodes = 'MTWUFAS'
        self.weekdays = []
        for d in meetdays:
            found_code = False
            for n in range(0, len(daycodes)):
                if daycodes[n]==d:
                    self.weekdays.append(n)
                    found_code = True
            if found_code==False:
                print('Warning: Could not match string \"' + d + '\" to a weekday code')

    def next_free_date(self):
        foundDate = False
        for delta in range(1, 365):
            dt1 = self.last_date + datetime.timedelta(delta)
            
            # First check if class usually meets on this day
            isMeetDay = False
            for m in self.weekdays:
                if dt1.weekday()==m:
                    isMeetDay = True
            
            # If so, check if it's a holiday
            if isMeetDay:
                isHoliday = False
                for hol in self.holidays:
                    # If it is a holiday, add holiday to the list of events
                    if hol[0]==dt1:
                        isHoliday = True
                        holitem = content('holiday', hol[1])
                        holitem.date = hol[0]
                        self.events.append(holitem)
            
            # If it is a valid class day, break out of the loop
            if isMeetDay and (not isHoliday):
                foundDate = True
                break
        if foundDate:
            return dt1
        else:
            return -1
    
    def add_holiday(self, datestring, htitle):
        self.holidays.append([date.fromisoformat(datestring), htitle])
        # If we've already scheduled events LATER than the new holiday
        # we need to re-schedule:
        if self.last_date >= date.fromisoformat(datestring):
            old_event_list = self.events
            self.events = []
            self.last_date = self.start_date + datetime.timedelta(-1)
            for item in old_event_list:
                if item.cformat != 'holiday':
                    self.add_content(item)
                
    def add_content(self, item):
        dt = self.next_free_date()
        item.date = dt
        self.events.append(item)
        self.last_date = item.date
                
    def print_events(self):
        week = 0
        module = 0
        lastday = 8
        mdtext = 'Welcome to Physical Chemistry Laboratory!<br><br> This site hosts Jupyter Notebooks where you can upload, import, and analyze your experimental data and write electronic lab reports for each laboratory period. The schedule below will be updated each week with links to the relevant notebook sessions.'
        for item in self.events:
            if item.isnew:
                module += 1
                mdtext += "\r"
                mdtext += '## Experiment ' + str(module) + " \r"
#             if item.date.weekday() < lastday:
#                 week += 1
#                 mdtext += '#### Week ' + str(week) + "\r"
#             lastday = item.date.weekday()
            datetext = " * <b>" + item.date.strftime("%b %-d") + "</b>: "
            
            holiday_color = 'Purple'
            #lecture_color = '#3090C7'
            lecture_color='Black'
            compute_color = 'DarkBlue'
            
            if item.cformat=='holiday':
                titlecol = holiday_color
            elif item.cformat=='lecture':
                titlecol = lecture_color
            elif item.cformat=='bye':
                titlecol = bye_color
            elif item.cformat=='compute':
                titlecol = compute_color
            else:
                titletext = item.title
                
            if len(item.link)>0 and item.cformat=='lecture':
                titletext = "<a href=\""+ item.link + "\"> <span style=\"color:" + titlecol + ";text-decoration:underline\">" + item.title + "</span></a>"
            elif len(item.link)>0 and item.cformat=='preview':
                titletext = "<a href=\""+ item.link + "\" style=\"text-decoration: none\"> <span style=\"color:" + titlecol + "\">" + item.title + "</span></a>"
            else:
                titletext = "<span style=\"color:" + titlecol + "\">" + item.title + "</span>"
                #titletext = '[' + titletext + '](' + item.link + ')'
            
            if len(item.vlink)>0:
                titletext += ' ([video](' + item.vlink + '))'
            
                
            mdtext += datetext + titletext + " \r\r"
        display_markdown(mdtext, raw=True)
        
class content:
    def __init__(self, cformat, title, newtopic=False, link='', vlink=''):
        self.cformat = cformat
        self.title = title
        self.link = link
        self.vlink = vlink
        self.date = -1
        self.isnew = newtopic


def build_schedule_f2021(srcdir):
    schd = schedule('M', '2021-08-23')

#     schd.add_holiday('2021-09-06', 'Labor Day')
    schd.add_holiday('2021-10-11', 'October Break (No labs)')
    schd.add_holiday('2021-10-12', 'October Break (No labs)')
    schd.add_holiday('2021-11-22', 'Thanksgiving (No labs)')
    
#     schd.add_holiday('2021-12-13', 'Finals')
#     schd.add_holiday('2021-12-14', 'Finals')
#     schd.add_holiday('2021-12-15', 'Finals')
#     schd.add_holiday('2021-12-16', 'Finals')
#     schd.add_holiday('2021-12-17', 'Finals')
#     schd.add_holiday('2021-12-18', 'Finals')

    schd.add_content(content('lecture', 'Group A: Temp. Sensors and Computer Analysis', newtopic=True, link=srcdir+'TempSensors/temp_sensors_main.ipynb'))
    schd.add_content(content('lecture', 'Group B: Temp. Sensors and Computer Analysis', link=srcdir+'TempSensors/temp_sensors_main.ipynb'))
    
    schd.add_content(content('lecture', 'Group A: Electronic Spectroscopy Part 1', newtopic=True, link=srcdir+'UVVis/uvvis_main_a.ipynb'))
    schd.add_content(content('lecture', 'Group A: Electronic Spectroscopy Part 2', newtopic=False, link=srcdir+'UVVis/uvvis_main_b.ipynb'))
    schd.add_content(content('lecture', 'Group B: Electronic Spectroscopy Part 1', link=srcdir+'UVVis/uvvis_main_a.ipynb'))
    schd.add_content(content('lecture', 'Group B: Electronic Spectroscopy Part 2', link=srcdir+'UVVis/uvvis_main_b.ipynb'))
    
    schd.add_content(content('lecture', 'Group A: Gas Phase Kinetics Part 1', newtopic=True, link=srcdir+'Kinetics/kinetics_main_a.ipynb'))
    schd.add_content(content('lecture', 'Group A: Gas Phase Kinetics Part 2', link=srcdir+'Kinetics/kinetics_main_b.ipynb'))
    schd.add_content(content('lecture', 'Group B: Gas Phase Kinetics Part 1', link=srcdir+'Kinetics/kinetics_main_a.ipynb'))
    schd.add_content(content('lecture', 'Group B: Gas Phase Kinetics Part 1', link=srcdir+'Kinetics/kinetics_main_b.ipynb'))
    
    schd.add_content(content('lecture', 'Group A: Joule Thomson Part 1', newtopic=True, link=srcdir+'JouleThomson/joule_thomson_main_a.ipynb'))
    schd.add_content(content('lecture', 'Group A: Joule Thomson Part 2', link=srcdir+'JouleThomson/joule_thomson_main_b.ipynb'))
    schd.add_content(content('lecture', 'Group B: Joule Thomson Part 1'))
    schd.add_content(content('lecture', 'Group B: Joule Thomson Part 2'))
    
#     schd.add_content(content('lecture', 'Freedom!'))
    return schd
