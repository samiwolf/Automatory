import json, requests
from bs4 import BeautifulSoup

import os
import re
from Database.MongoDB import db
from subprocess import Popen, PIPE, CalledProcessError

collection = db.TESTSSL
collection_banks = db.DOMAINS_BANKS
collection_pubuni = db.DOMAINS_PUBLIC_UNIVERSITIES
collection_priuni = db.DOMAINS_PRIVATE_UNIVERSITIES
collection_pubmed = db.DOMAINS_PUBLIC_MEDICAL_COLLEGE
collection_primed = db.DOMAINS_PRIVATE_MEDICAL_COLLEGE




def scan(domain):
    script_dir = os.path.dirname(__file__)
    checkCmd = os.path.join(script_dir, "testssl.sh/testssl.sh")
    args = [checkCmd, '--quiet', domain]
    check = Popen(args, stdout=PIPE, stderr=PIPE, stdin=PIPE)

    output, err = check.communicate(input=b'yes')
    renderer = Popen('aha', stdin=PIPE, stdout=PIPE, stderr=PIPE)
    html, err = renderer.communicate(input=output)
    return html


def banks_db():
    collection_news = db.DOMAINS_BANKS
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain': domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)


def news_db():
    collection_news = db.DOMAINS_NEWSPAPERS
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain':domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)


def pub_uni_db():
    collection_news = db.DOMAINS_PUBLIC_UNIVERSITIES
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain': domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)


def pri_uni_db():
    collection_news = db.DOMAINS_PRIVATE_UNIVERSITIES
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain': domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)


def pub_medi_db():
    collection_news = db.DOMAINS_PUBLIC_MEDICAL_COLLEGE
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain': domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)


def pri_medi_db():
    collection_news = db.DOMAINS_PRIVATE_MEDICAL_COLLEGE
    cursor = collection_news.find({})

    for document in cursor:
        domain = document['domain']

        if not collection.find_one({'domain': domain}):
            result = scan(domain)
            dict = {'domain': domain,
                    'result': result}
            collection.insert_one(dict)
            print(dict)

banks_db()
pub_uni_db()
pri_uni_db()
pub_medi_db()
pri_medi_db()
