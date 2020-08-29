import scrapy
from recipeItem import RecipeItem
import json


#Usage: scrapy runspider woksOfLifeSpider.py -o wol_recipes.json > woksoflife_out.log 2>&1
class WoksOfLifeTestSpider(scrapy.Spider):
	name = 'recipes'
	start_urls = [
		'https://thewoksoflife.com/chinese-preserved-greens/',
		'https://thewoksoflife.com/recipe-list/?category=quick-and-easy'
	]

	def parse(self, response):
		if "recipe-list" in response.request.url:
			relatedPosts = response.css('.kd-listing *::attr(href)').getall()
			for li in response.css('.kd-ind-list').css('a::attr(href)').getall():
				print(li)
			# print(relatedPosts)


	def relatedParse(self, response):

		print("Printing debug output:")

		#Download related recipes
		relatedPosts = response.css('.relpost-block-single::attr(href)').getall()			
		print(relatedPosts)