
from parser.lawyer import LawyerType
from parser.scrapper import LawlyScrapperSource
from parser.scrapper import LawlyJSON
from parser.profiler import profile


class LawlyMapper:
    _valid_lawyers = []
    _invalid_lawyers = []

    def __init__(self):
        self._set_lawyers()

    def _set_lawyers(self):
        for source in LawlyScrapperSource:
            # only Outputs
            source_list_name = LawlyScrapperSource.lawyer_list_cat(source)
            if source_list_name != 'output_data':
                continue

            my_parser = LawlyJSON(source)
            lawyers = my_parser.get_lawyers(LawyerType.Lawyer)
            for lawyer in lawyers:
                if lawyer:
                    self._valid_lawyers.append(lawyer)
                else:
                    self._invalid_lawyers.append(lawyer)

    @profile
    def map(self):
        mapped = []

        valid_valid = LawlyMapper._find_similar(self.valid_lawyers, self.valid_lawyers, keep_unpaired=False)
        valid_valid_mapped = []
        for pair in valid_valid:
            valid = pair[0]
            mapped_lawyer = None
            for invalid in pair[1]:
                if invalid is None:
                    mapped_lawyer = valid
                else:
                    mapped_lawyer = valid.merge(invalid)

            if mapped_lawyer is not None and mapped_lawyer:
                valid_valid_mapped.append(mapped_lawyer)

        valid_invalid = LawlyMapper._find_similar(valid_valid_mapped, self.invalid_lawyers, keep_unpaired=True)
        for pair in valid_invalid:
            valid = pair[0]
            mapped_lawyer = None
            for invalid in pair[1]:
                if invalid is None:
                    mapped_lawyer = valid
                else:
                    mapped_lawyer = valid.merge(invalid)

            if mapped_lawyer is not None and mapped_lawyer:
                mapped.append(mapped_lawyer)

        return mapped

    @property
    def valid_lawyers(self):
        return self._valid_lawyers

    @property
    def invalid_lawyers(self):
        return self._invalid_lawyers

    @staticmethod
    def _find_similar(search_list, find_in_list, keep_unpaired):
        similar = []

        cur_find_in_list = find_in_list.copy()

        ind = 1
        for search_item in search_list:
            print('processing: ', str(ind), '/', str(len(search_list)), '/', str(len(similar)))

            new_find_in_list = []
            similar_items = []
            for find_item in cur_find_in_list:
                if search_item == find_item:
                    similar_items.append(find_item)
                else:
                    new_find_in_list.append(find_item)
            cur_find_in_list = new_find_in_list.copy()

            if similar_items:
                similar.append([search_item, similar_items])
            elif keep_unpaired:
                similar.append([search_item, [None]])

            ind += 1

        return similar
