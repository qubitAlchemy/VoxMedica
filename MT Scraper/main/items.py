import scrapy

class MtsamplesItem(scrapy.Item):
	medical_specialty = scrapy.Field()
	sample_name = scrapy.Field()
	description = scrapy.Field()
	transcription = scrapy.Field()
	pass
