
from parser.lawyer import LawyerType
from parser.lawyer import LawyerAddress
import parser.scrapper as parser
import parser.mapper as mapper

import datetime
import numpy as np
import pandas as pd


class LawlyBuilder:

    def __init__(self):
        self._state = 0

    def build(self):
        self._state = 1
        self._run_api()
        self._run_scrapper()
        self._run_mapper()
        self._run_updater()
        self._run_rebuilder()
        self._load_lawyers_json()
        self._load_lawyers_txt()
        self._show_stats()

    @staticmethod
    def _run_api():

        def erau():
            my_parser = parser.LawlyAPIERAU()
            lawyers = my_parser.get_lawyers(LawyerType.Attorney)
            if not lawyers:
                print('ERAU: Lawyers could not be found')
                return
            my_parser.save_json(lawyers)

        def ern():
            my_parser = parser.LawlyAPIERN()
            lawyers = my_parser.get_lawyers(LawyerType.Notary)
            if not lawyers:
                print('ERN: Lawyers could not be found')
                return
            my_parser.save_json(lawyers)

        erau()
        ern()

    @staticmethod
    def _run_scrapper():

        def get_lawyers(new_parser, name):
            lawyers = new_parser.get_lawyers(LawyerType.Lawyer)
            if not lawyers:
                print(name, ': Lawyers could not be found')
                return
            new_parser.save_json(lawyers)

        def freelawyer():
            get_lawyers(parser.LawlyScrapperFreeLawyer(), 'FreeLawyer')

        def atty():
            get_lawyers(parser.LawlyScrapperAtty(), 'Atty')

        def lawyerua():
            get_lawyers(parser.LawlyScrapperLawyerUA(), 'LawyerUA')

        def protocol():
            get_lawyers(parser.LawlyScrapperProtocol(), 'Protocol')

        def notarykiev():
            get_lawyers(parser.LawlyScrapperNotaryKiev(), 'NotaryKiev')

        def notarykievua():
            get_lawyers(parser.LawlyScrapperNotaryKievUA(), 'NotaryKievUA')

        def notaryua():
            get_lawyers(parser.LawlyScrapperNotaryUA(), 'NotaryUA')

        def jurliga():
            get_lawyers(parser.LawlyScrapperJurliga(), 'Jurliga')

        def notary2gis():
            get_lawyers(parser.LawlyScrapperNotary2gis(), '2gis')

        def leegl():
            get_lawyers(parser.LawlyScrapperLeegl(), 'Leegl')

        def czech():
            get_lawyers(parser.LawlyScrapperCzech(), 'Czech')

        def poland():
            get_lawyers(parser.LawlyScrapperPoland(), 'Poland')

        freelawyer()
        atty()
        lawyerua()
        protocol()
        notarykiev()
        notarykievua()
        notaryua()
        notary2gis()
        jurliga()
        leegl()
        czech()
        poland()

    @staticmethod
    def _run_mapper():
        my_mapper = mapper.LawlyMapper()
        mapped_lawyers = my_mapper.map()

        my_parser = parser.LawlyParser(
            parser_type=parser.LawlyParserType.JSON,
            output_source=parser.LawlyScrapperSource.ValidLawyers
        )
        my_parser.save_json(mapped_lawyers)

    @staticmethod
    def _run_updater():
        my_parser = parser.LawlyJSON(parser.LawlyScrapperSource.ValidLawyers)
        lawyers = my_parser.get_lawyers(LawyerType.Lawyer)
        if not lawyers:
            return

        count = 0
        my_updater = parser.LawlyScrapperERAU()
        for lawyer in lawyers:
            count += 1
            print('processing:', count, '/', len(lawyers))

            if lawyer.type == LawyerType.Attorney:
                my_updater.update_lawyer(lawyer)
            elif lawyer.type == LawyerType.Notary:
                if lawyer.verification:
                    lawyer.update('status', 'True')

        my_parser = parser.LawlyParser(
            parser_type=parser.LawlyParserType.JSON,
            output_source=parser.LawlyScrapperSource.ValidLawyers
        )
        my_parser.save_json(lawyers)

    @staticmethod
    def _run_rebuilder():
        my_parser = parser.LawlyJSON(parser.LawlyScrapperSource.ValidLawyers)
        lawyers = my_parser.get_lawyers(LawyerType.Lawyer)
        if not lawyers:
            return

        new_lawyers = []
        for lawyer in lawyers:
            cur_address = lawyer.address
            if cur_address.area.find('Київ') >= 0 \
                or cur_address.area.find('Киев') >= 0 \
                or cur_address.town.find('Київ') >= 0 \
                or cur_address.town.find('Киев') >= 0:

                new_address = LawyerAddress(
                    country=cur_address.country,
                    area='Київ  область',
                    region=cur_address.region,
                    town='Киев',
                    street=cur_address.street,
                    street_type=cur_address.street_type,
                    street_number=cur_address.street_number,
                    apartment_type=cur_address.apartment_type,
                    apartment_number=cur_address.apartment_number,
                    postal_code=cur_address.postal_code
                )
                lawyer.update('address', new_address)

                new_lawyers.append(lawyer)

        my_parser.save_json(new_lawyers)

    @staticmethod
    def _load_lawyers_json():

        def get_lawyers(source):
            my_parser = parser.LawlyJSON(source)
            lawyers = my_parser.get_lawyers(LawyerType.Lawyer)
            if not lawyers:
                print('Lawyers could not be found')
                return

        def freelawyer():
            get_lawyers(parser.LawlyScrapperSource.FreeLawyer_Output)

        def atty():
            get_lawyers(parser.LawlyScrapperSource.Atty_Output)

        def lawyerua():
            get_lawyers(parser.LawlyScrapperSource.LawyerUA_Output)

        def protocol():
            get_lawyers(parser.LawlyScrapperSource.Protocol_Output)

        def notarykeiv():
            get_lawyers(parser.LawlyScrapperSource.NotaryKiev_Output)

        def notaryua():
            get_lawyers(parser.LawlyScrapperSource.NotaryUA_Output)

        def jurliga():
            get_lawyers(parser.LawlyScrapperSource.Jurliga_Output)

        def czech():
            get_lawyers(parser.LawlyScrapperSource.Czech_Output)

        def poland():
            get_lawyers(parser.LawlyScrapperSource.Poland_Output)


        freelawyer()
        atty()
        lawyerua()
        protocol()
        notarykeiv()
        notaryua()
        jurliga()
        czech()
        poland()

    @staticmethod
    def _load_lawyers_txt():
        find_path = '/Contact/Details/'
        lawyers = []
        with open(r'D:\Projects\lawly\Parser\input_data\czech_input.txt', 'r', encoding='utf-8') as f:
            text = f.read()
            while True:
                start = text.find(find_path)
                if start == -1:
                    break
                finish = text.find('"', start)
                profile_id = text[start + len(find_path):finish]
                lawyers.append(profile_id)

                full_path = find_path + profile_id
                text = text.replace(full_path, '')

        with open(r'D:\Projects\lawly\Parser\input_data\czech_output.txt', 'w', encoding='utf-8') as f:
            for profile_id in lawyers:
                f.write(profile_id + '\n')

    @staticmethod
    def _show_stats():
        my_parser = parser.LawlyJSON(parser.LawlyScrapperSource.ValidLawyers)
        lawyers = my_parser.get_lawyers(LawyerType.Lawyer)
        if not lawyers:
            return

        emails = []
        phones = []

        with_specs = 0
        with_email = 0
        with_address = 0
        with_phones = 0
        with_contacts = 0
        law_count = 0
        att_count_active = 0
        att_count_disabled = 0
        not_count = 0
        for lawyer in lawyers:
            if lawyer.type == LawyerType.Lawyer:
                law_count += 1
            if lawyer.type == LawyerType.Attorney:
                if lawyer.status is None or not lawyer.status:
                    att_count_disabled += 1
                else:
                    att_count_active += 1
            if lawyer.type == LawyerType.Notary:
                not_count += 1
            if lawyer.address.street:
                with_address += 1
            if lawyer.phones:
                with_phones += 1
                for phone in lawyer.phones:
                    phones.append(phone)
            if lawyer.email and lawyer.address.street and lawyer.phones:
                with_contacts += 1
            if lawyer.specializations:
                with_specs += 1
            if lawyer.email:
                emails.append(lawyer.email)
                with_email += 1

        emails = list(set(emails))
        emails_df = pd.DataFrame(emails)
        emails_df.to_csv('emails.csv', index=False)

        phones = list(set(phones))
        phones_df = pd.DataFrame(phones)
        phones_df.to_csv('phones.csv', index=False)

        print('Total valid lawyers:', len(lawyers))
        print(
            'Attorneys:', att_count_active + att_count_disabled,
            '| Active:', att_count_active,
            '| Disabled:', att_count_disabled
        )
        print('Notaries:', not_count)
        print('Lawyers:', law_count)
        print('With address:', with_address)
        print('With email:', with_email)
        print('With phone:', with_phones)
        print('Full contacts:', with_contacts)
        print('Specs:', with_specs)
