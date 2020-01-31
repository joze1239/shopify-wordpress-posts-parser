import json
import csv
import arrow
import requests
from bs4 import BeautifulSoup
import re

authors = {
    "Emily Bertha": "emilybertha",
    "Guest Writer": "eightguestwriter",
    "Alex Pinarello": "eightalexpinarello",
    "Carlie Dobkin": "eightcarliedobkin",
    "Lucid Fusion Collaborator": "eightguestwriter",
    "Alexandra Zatarain": "eightalexandrazatarain",
    "Eight Collaborator": "eightguestwriter",
    "Matteo Franceschetti": "eightmatteofranceschetti"
}

with open('out.csv', mode='w') as csv_file:
    fieldnames = ['post_title', 'ID', 'post_content', 'post_excerpt', 'post_date', 'post_name', 'post_author',
                  'post_publisher',
                  'post_status', 'featured_image', 'post_format', 'comment_status', 'ping_status', 'post_category',
                  'post_tag', 'seo_description'
                  ]
    writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
    writer.writeheader()

    with open('blog_articles_30012019.json') as json_file:
        data = json.load(json_file)
        count = 0
        for a in data['articles']:
            count += 1
            #if count > 20:
            #    continue

            r = requests.get('http://eightsleep.com/blogs/news/' + a['handle'])
            print(r.status_code)
            
            if r.status_code == 404:
                print('404: Post: ' + str(a['id']), a['title'], a['handle'], date_str)
                continue
            
            soup = BeautifulSoup(r.text, 'html.parser')
            desc = soup.findAll(attrs={"name": re.compile(r"description", re.I)}) 
            meta_description = desc[0]['content']
            
            image_url = ''
            if 'image' in a:
                image_url = a['image']['src']

            date = arrow.get(a['created_at'])
            d = date.datetime

            dMinute = ("0" + str(d.minute) if d.minute < 10 else str(d.minute))
            date_str = str(d.month) + "/" + str(d.day) + "/" + str(d.year) + " " + str(d.hour) + ":" + dMinute

            print('Post: ' + str(a['id']), a['title'], a['handle'], date_str)
            writer.writerow({
                'post_title': a['title'],
                'ID': str(a['id']),
                'post_content': a['body_html'],
                'post_excerpt': '',
                'post_date': date_str,
                'post_name': a['handle'],
                'post_author': authors[a['author']],
                'post_publisher': a['author'],
                'post_status': 'publish',
                'featured_image': image_url,
                'post_format': '',
                'comment_status': 'open',
                'ping_status': 'open',
                'post_category': 'Uncategorized',
                'post_tag': a['tags'],
                'seo_description': meta_description
            })