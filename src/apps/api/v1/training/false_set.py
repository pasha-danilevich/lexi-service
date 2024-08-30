import random

from django.db.models import Count
from apps.word.models import PartOfSpeech, Translation


class FalseSet():
    
    def __init__(self, queryset, word_count: int):
        self.word_count = word_count
        self.keys_to_keep = ['сущ', 'гл', 'нареч', 'прил', 'прич']
        self.counted_pos_word = self._clear_pos(self._get_counted_pos(queryset))
    
        self.pos_id = self._get_dict_pos_id(self.counted_pos_word)
        self.counted_pos_bd = self._count_pos_bd(self.counted_pos_word)
        self.false_set_by_pos = self._get_false_set_by_pos(
            self.counted_pos_word, 
            self.counted_pos_bd
        )
        
    def _get_counted_pos(self, obj: list[dict]) -> dict[str, int]:
        dictionary_query_set = obj
        counted_part_of_speech = {}
        for item in dictionary_query_set:
            pos = item['word__part_of_speech__text']
            existen_pos = counted_part_of_speech.get(pos, None)
            if existen_pos:
                counted_part_of_speech[pos] += 1
            else:
                counted_part_of_speech.update({pos:1})
                existen_pos = None
        return counted_part_of_speech
    
    def _clear_pos(self, dict: dict) -> dict[str, int]:

        clear_dict = {'сущ': 0}
        
        for k, v in dict.items():
            if k in self.keys_to_keep:
                clear_dict[k] = v
            else:
                clear_dict['сущ'] += dict[k]   

        return clear_dict
    
    def _get_dict_pos_id(self, counted_pos_word: dict[str, int])-> dict[str, int]:
        part_of_speech_list = PartOfSpeech.objects.filter(
            text__in=self.keys_to_keep
        )

        pos_id = {
            part['text']: part['id'] 
            for part 
            in part_of_speech_list.values('text', 'id')
        }
        
        return pos_id
    
    def _count_pos_bd(self, counted_pos_word: dict[str, int]):
        result = {
            k: v 
            for k, v in PartOfSpeech.objects
                .filter(text__in=counted_pos_word.keys())
                .annotate(word_count=Count('translations__id'))  # Исправлено здесь
                .values_list('text', 'word_count')
        }
        return dict(result)
    
    def _get_false_set_by_pos(
        self, 
        counted_pos_word: dict[str, int], 
        counted_pos_bd: dict[str, int]
    ) -> dict[str, str]:
        result = {}
        for pos, count in counted_pos_bd.items():
            if count > 0:
                offset = random.randint(0, max(0, count - self.word_count))  # Убедимся, что OFFSET не превышает количество записей
                stack_word_list = Translation.objects.filter(
                    part_of_speech_id=self.pos_id[pos]
                ).values_list('text', flat=True)[
                    offset:offset + self.word_count * counted_pos_word[pos]
                ]
                
                result.update({pos: list(stack_word_list)})
                           
        return result
    
    def _pop_random_element(self, dictionary, key) -> str | None:
        # эту функцию надо удибарь в Falset
        if key in dictionary and dictionary[key]:
            # Выбираем случайный элемент
            random_element = random.choice(dictionary[key])
            # Удаляем элемент из списка
            dictionary[key].remove(random_element)
            return random_element
        else:
            return None  # Если ключа нет или список пустой
        
    def get_list_false_set_word(self, pos):
        list_false_set_word = []
        for _ in range(self.word_count):
            word = self._pop_random_element(
                    dictionary=self.false_set_by_pos,
                    key=pos
                )
            if not word:
                word = self._pop_random_element(
                    dictionary=self.false_set_by_pos,
                    key='сущ'
                )
            list_false_set_word.append(word)
        print(self.false_set_by_pos)
        return list_false_set_word