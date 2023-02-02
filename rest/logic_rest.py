import statistics

from django.db.models import Avg
from django.db.models import Q
from django.db.models import QuerySet
from django.template.backends import django

from rest.models import Restaurants


class UtilityRest():

    def get_all_restaurants_range(self,latitude:float,longitud:float,range:float)->QuerySet:

        sql_query ='''select rest.id from rest_restaurants as rest 
                    where (SQRT(power((rest.lng - %s ),2) 
                    +power((rest.lat - %s ),2) ))*110 < %s'''

        # Restaurants.objects.extra()
        id_list =[]
        raw_query = Restaurants.objects.raw(sql_query, [longitud, latitude, range])
        for rest in raw_query: id_list.append(rest.id)
        list_rest = Restaurants.objects.filter(Q(id__in = id_list))
        return list_rest

    def get_restaurants_statistics(self,list_rest:QuerySet)-> dict:
        count= list_rest.count()
        avg = list_rest.aggregate(Avg('rating'))["rating__avg"]
        std = statistics.stdev(list_rest.values_list('rating', flat=True))
        data_out ={
                "count":count,
                "avg" : avg,
                "std" : std
                }
        return data_out

    def get_all_restaurant(self)->list:
        data_out = []
        list_rest = Restaurants.objects.filter()
        for rest in list_rest:
            data_out.append(rest.get_rest_info())
        return data_out