import datetime
import json

# import requests
# from path import Path


heroes_json = json.load(open(r'D:\用户目录\Temp\Kabam Montreal, Inc\Shop Titans\data\heroes.json'))
quests_json = json.load(open(r'D:\用户目录\Temp\Kabam Montreal, Inc\Shop Titans\data\quests.json'))

eventDict = {
    "lcog": {
        "start": 172800000,
        "end": 345600000,
        "offset": 28 * 24 * 60 * 60 * 1000
    },
    "titantower": {
        "start": 1382400000,
        "end": 1555200000,
        "offset": 28 * 24 * 60 * 60 * 1000
    },
    "king": {
        "start": 604800000,
        "end": 1209600000,
        "offset": 28 * 24 * 60 * 60 * 1000
    }
}


class calendar:
    def __init__(self):
        self.cal = {}
        now=datetime.datetime.now()
        self.beginDate=datetime.datetime(year=now.year,month=now.month,day=now.day,
                                    hour=0,minute=0,second=0,microsecond=0)


        pass
    def to_do(self):
        self._match_heros()
        self.write_csv()
        pass
    def _match_heros(self):

        for hero in heroes_json:
            print(hero)
            self.cal.update(self._match_one_hero(hero_dct=heroes_json[hero]))

        print()
    def _match_one_hero(self,hero_dct:dict):
        time_offset=(self.beginDate.timestamp()*1000)%hero_dct['respawnCycle']
        first_time=((self.beginDate.timestamp()*1000)-time_offset+hero_dct['respawnOffset'])/1000

        # first_time =( int((self.beginDate.timestamp()*1000)/hero_dct['respawnCycle']+1)*hero_dct['respawnCycle']+hero_dct['respawnOffset']) / 1000

        sep=hero_dct['respawnCycle']/1000
        first_datetime=datetime.datetime.fromtimestamp(first_time)
        sep_time=datetime.timedelta(seconds=sep)

        first_datetime.strftime('r%Y/%m/%d %H:%M:%S')
        # sep_time.total_seconds()
        # sep_time.__str__()
        sep_time.total_seconds()

        return {hero_dct['uid']:{"first_time":first_datetime,"sep":sep_time,'bulkTypes':hero_dct['bulkTypes']}}

    def write_csv(self):
        with open('1.csv',mode='w',encoding='utf-8') as fn:
            line="Title,Category,Description,Start,Duration,Popup Reminder Time,Recurrence"
            fn.write(line+'\n')

            for hero in self.cal:
                dct=self.cal[hero]
                line=[dct['bulkTypes'].replace(',','|'),'勇士',hero,dct['first_time'].strftime('%Y/%m/%d %H:%M:%S'),'30 min','1 hour',f"{dct['sep'].total_seconds()} second"]
                fn.write(','.join(line).strip(',') + '\n')





if __name__ == '__main__':
    cls=calendar()
    cls.to_do()


    print(1)
