import json
from django.core import serializers
from channels.generic.websocket import AsyncWebsocketConsumer
from django.db.models import ObjectDoesNotExist
from .models import CountryData
from channels.db import database_sync_to_async


class DashboardConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = 'dashboard'
        self.room_group_name = f"dashboard_group"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        
        print(f"text data json is {text_data_json}")
        country = text_data_json.get('country')
        population = text_data_json.get('population')

        if 'id' in text_data_json:
            result = await self.update_country_data(text_data_json['id'], population)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chart_update',
                    'updated_country': result
                }
            )
        else:
            result = await self.create_country_data(country, population)
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chart_new',
                    'new_country': result
                }
            )
            
    async def chart_update(self, event) -> None:
        country_obj = event.get('updated_country')

        await self.send(text_data=json.dumps({
            'type': 'chart_update',
            'country': country_obj['country'],
            'population': country_obj['population'],
        }))

    async def chart_new(self, event) -> None:
        country_obj = event.get('new_country')

        await self.send(text_data=json.dumps({
            'type': 'chart_new',
            'country': country_obj['country'],
            'population': country_obj['population'],
        }))

    @database_sync_to_async
    def update_country_data(self, id, population):
        try:
            country = CountryData.objects.get(id=id)
            country.population = population
            country.save()
            return {'country': country.country, 'population': country.population}
        except ObjectDoesNotExist:
            return None

    @database_sync_to_async
    def create_country_data(self, country_name, population):
        try:
            country = CountryData.objects.create(country=country_name, population=population)
            return {'country': country.country, 'population': country.population}
        except ObjectDoesNotExist:
            return None
