
import json
from decimal import Decimal, InvalidOperation
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect

from .models import UserProfile, CheckoutDetails, Order, OrderItem
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4

from .models import Order, CheckoutDetails
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import CheckoutDetails

def home(request):
    show_home_login_success = request.session.pop(
        'show_home_login_success', False
    )
    return render(
        request,
        'shop/index.html',
        {'show_home_login_success': show_home_login_success}
    )



def shop_page(request):
    query = request.GET.get('q', '').strip()

    products = [
        {
            'name': 'Scientific Calculator',
            'slug': 'scientific-calculator',
            'image': 'shop/images/product-calculator.png',
            'price': 50,
        },
        {
            'name': 'Stapler',
            'slug': 'stapler',
            'image': 'shop/images/product-stapler.png',
            'price': 100,
        },
        {
            'name': 'Desk Organizer',
            'slug': 'desk-organizer',
            'image': 'shop/images/office1.webp',
            'price': 120,
        },
        {
            'name': 'Pen Set',
            'slug': 'pen-set',
            'image': 'shop/images/product-pens.png',
            'price': 50,
        },
        {
            'name': 'Scissors',
            'slug': 'scissors',
            'image': 'shop/images/product-scissors.png',
            'price': 60,
        },
        {
            'name': 'Office Supplies Set',
            'slug': 'office-supplies-set',
            'image': 'shop/images/office2.jpeg',
            'price': 90,
        },
        {
            'name': 'Highlighter Set',
            'slug': 'highlighter-set',
            'image': 'shop/images/hero-highlighters.png',
            'price': 70,
        },
        {
            'name': 'Desk Accessories',
            'slug': 'desk-accessories',
            'image': 'shop/images/office3.jpeg',
            'price': 150,
        },
        {
            'name': 'Notebook Set',
            'slug': 'notebook-set',
            'image': 'shop/images/office4.jpeg',
            'price': 80,
        },
        {
            'name': 'Paper Stationery',
            'slug': 'paper-stationery',
            'image': 'shop/images/paper1.jpeg',
            'price': 50,
        },
        {
            'name': 'Notebook Accessories',
            'slug': 'notebook-accessories',
            'image': 'shop/images/paper2.jpeg',
            'price': 110,
        },
        {
            'name': 'Writing and Paper Set',
            'slug': 'writing-paper-set',
            'image': 'shop/images/paper3.jpeg',
            'price': 130,
        },
    ]

    if query:
        search_text = ''.join(query.casefold().split())

        products = [
            product
            for product in products
            if search_text in ''.join(
                product['name'].casefold().split()
            )
        ]

    return render(
        request,
        'shop/shop.html',
        {
            'products': products,
            'search_query': query,
        }
    )



def global_product_search(request):
    query = request.GET.get('q', '').strip()

    products = [
        # Office Basics
        {'name': 'Scientific Calculator', 'slug': 'scientific-calculator', 'image': 'shop/images/product-calculator.png', 'price': 50},
        {'name': 'Stapler', 'slug': 'stapler', 'image': 'shop/images/product-stapler.png', 'price': 100},
        {'name': 'Desk Organizer', 'slug': 'desk-organizer', 'image': 'shop/images/office1.webp', 'price': 120},
        {'name': 'Pen Set', 'slug': 'pen-set', 'image': 'shop/images/product-pens.png', 'price': 50},
        {'name': 'Scissors', 'slug': 'scissors', 'image': 'shop/images/product-scissors.png', 'price': 60},
        {'name': 'Office Supplies Set', 'slug': 'office-supplies-set', 'image': 'shop/images/office2.jpeg', 'price': 90},
        {'name': 'Highlighter Set', 'slug': 'highlighter-set', 'image': 'shop/images/hero-highlighters.png', 'price': 70},
        {'name': 'Desk Accessories', 'slug': 'desk-accessories', 'image': 'shop/images/office3.jpeg', 'price': 150},
        {'name': 'Notebook Set', 'slug': 'notebook-set', 'image': 'shop/images/office4.jpeg', 'price': 80},
        {'name': 'Paper Stationery', 'slug': 'paper-stationery', 'image': 'shop/images/paper1.jpeg', 'price': 50},
        {'name': 'Notebook Accessories', 'slug': 'notebook-accessories', 'image': 'shop/images/paper2.jpeg', 'price': 110},
        {'name': 'Writing and Paper Set', 'slug': 'writing-paper-set', 'image': 'shop/images/paper3.jpeg', 'price': 130},

        # Files & Folders
        {'name': 'File Folder', 'slug': 'file-folder', 'image': 'shop/images/files1.jpeg', 'price': 80},
        {'name': 'Document Folder', 'slug': 'document-folder', 'image': 'shop/images/files2.jpeg', 'price': 120},
        {'name': 'Plastic File', 'slug': 'plastic-file', 'image': 'shop/images/files3.jpeg', 'price': 60},
        {'name': 'Ring Binder', 'slug': 'ring-binder', 'image': 'shop/images/files4.jpeg', 'price': 150},
        {'name': 'Office File', 'slug': 'office-file', 'image': 'shop/images/files5.jpeg', 'price': 90},
        {'name': 'Expanding File', 'slug': 'expanding-file', 'image': 'shop/images/files6.jpeg', 'price': 200},
        {'name': 'Button File', 'slug': 'button-file', 'image': 'shop/images/files7.jpeg', 'price': 50},
        {'name': 'Clear Folder', 'slug': 'clear-folder', 'image': 'shop/images/files8.jpeg', 'price': 100},
        {'name': 'Project File', 'slug': 'project-file', 'image': 'shop/images/files9.jpeg', 'price': 180},
        {'name': 'Lever Arch File', 'slug': 'lever-arch-file', 'image': 'shop/images/files10.jpeg', 'price': 250},
        {'name': 'Document Organizer', 'slug': 'document-organizer', 'image': 'shop/images/files11.jpeg', 'price': 300},
        {'name': 'File Collection', 'slug': 'file-collection', 'image': 'shop/images/files12.jpeg', 'price': 350},

        # Paper & Notebooks
        {'name': 'Notebook', 'slug': 'notebook', 'image': 'shop/images/paper1.jpeg', 'price': 100},
        {'name': 'Paper Notebook', 'slug': 'paper-notebook', 'image': 'shop/images/paper2.jpeg', 'price': 70},
        {'name': 'Drawing Paper', 'slug': 'drawing-paper', 'image': 'shop/images/paper3.jpeg', 'price': 140},
        {'name': 'Planner Notebook', 'slug': 'planner-notebook', 'image': 'shop/images/paper4.jpeg', 'price': 240},
        {'name': 'Writing Notebook', 'slug': 'writing-notebook', 'image': 'shop/images/paper5.jpeg', 'price': 270},
        {'name': 'Office Notebook', 'slug': 'office-notebook', 'image': 'shop/images/paper6.jpeg', 'price': 180},
        {'name': 'Notebook Set', 'slug': 'notebook-set-paper', 'image': 'shop/images/paper7.webp', 'price': 120},
        {'name': 'Study Notebook', 'slug': 'study-notebook', 'image': 'shop/images/paper8.jpeg', 'price': 90},
        {'name': 'Premium Notebook', 'slug': 'premium-notebook', 'image': 'shop/images/paper9.jpg', 'price': 80},
        {'name': 'Paper Collection', 'slug': 'paper-collection', 'image': 'shop/images/paper10.jpeg', 'price': 150},
        {'name': 'Creative Paper', 'slug': 'creative-paper', 'image': 'shop/images/paper11.jpg', 'price': 180},
        {'name': 'Notebook Collection', 'slug': 'notebook-collection', 'image': 'shop/images/paper12.jpg', 'price': 230},

        # Pens & Writing
        {'name': 'Blue Pen', 'slug': 'blue-pen', 'image': 'shop/images/pen1.jpeg', 'price': 90},
        {'name': 'Ball Pen', 'slug': 'ball-pen', 'image': 'shop/images/pen2.jpeg', 'price': 70},
        {'name': 'Color Pen', 'slug': 'color-pen', 'image': 'shop/images/pen3.jpeg', 'price': 80},
        {'name': 'Gel Pen', 'slug': 'gel-pen', 'image': 'shop/images/pen4.jpeg', 'price': 90},
        {'name': 'Writing Pen', 'slug': 'writing-pen', 'image': 'shop/images/pen5.jpeg', 'price': 60},
        {'name': 'Premium Pen', 'slug': 'premium-pen', 'image': 'shop/images/pen6.jpeg', 'price': 200},
        {'name': 'Pen Set', 'slug': 'pen-set-writing', 'image': 'shop/images/pen7.jpeg', 'price': 80},
        {'name': 'Sketch Pen', 'slug': 'sketch-pen', 'image': 'shop/images/pen8.jpeg', 'price': 70},
        {'name': 'Multicolor Pen', 'slug': 'multicolor-pen', 'image': 'shop/images/pen9.jpeg', 'price': 150},
        {'name': 'Marker Pen', 'slug': 'marker-pen', 'image': 'shop/images/pen10.jpeg', 'price': 90},
        {'name': 'Fine Tip Pen', 'slug': 'fine-tip-pen', 'image': 'shop/images/pen11.jpeg', 'price': 120},
        {'name': 'Pen Collection', 'slug': 'pen-collection', 'image': 'shop/images/pen12.jpeg', 'price': 100},

        # School Supplies
        {'name': 'School Supplies Set', 'slug': 'school-supplies-set', 'image': 'shop/images/school1.jpeg', 'price': 50},
        {'name': 'School Stationery', 'slug': 'school-stationery', 'image': 'shop/images/school2.jpeg', 'price': 120},
        {'name': 'Student Stationery', 'slug': 'student-stationery', 'image': 'shop/images/school3.jpeg', 'price': 250},
        {'name': 'School Kit', 'slug': 'school-kit', 'image': 'shop/images/school4.jpeg', 'price': 350},
        {'name': 'Student Kit', 'slug': 'student-kit', 'image': 'shop/images/school5.jpeg', 'price': 80},
        {'name': 'School Essentials', 'slug': 'school-essentials', 'image': 'shop/images/school6.jpeg', 'price': 180},
        {'name': 'Writing Supplies', 'slug': 'writing-supplies', 'image': 'shop/images/school7.jpeg', 'price': 220},
        {'name': 'School Accessories', 'slug': 'school-accessories', 'image': 'shop/images/school8.jpeg', 'price': 450},
        {'name': 'Learning Supplies', 'slug': 'learning-supplies', 'image': 'shop/images/school9.jpeg', 'price': 95},
        {'name': 'Classroom Supplies', 'slug': 'classroom-supplies', 'image': 'shop/images/school10.jpeg', 'price': 150},
        {'name': 'Study Materials', 'slug': 'study-materials', 'image': 'shop/images/school11.jpeg', 'price': 300},
        {'name': 'School Collection', 'slug': 'school-collection', 'image': 'shop/images/school12.jpeg', 'price': 400},
    ]

    search_text = ''.join(query.casefold().split())

    if search_text:
        products = [
            product for product in products
            if search_text in ''.join(product['name'].casefold().split())
        ]
    else:
        products = []

    return render(
        request,
        'shop/search_results.html',
        {
            'products': products,
            'search_query': query,
        }
    )

def product_details(request, product_slug):
    products = {
        'scientific-calculator': {
            'name': 'Scientific Calculator',
            'image': 'shop/images/product-calculator.png',
            'price': 50,
            'description': 'A useful scientific calculator for students and professionals.',
            'features': [
                'Easy-to-use buttons',
                'Suitable for school and office use',
                'Compact and lightweight design',
            ],
        },
        'stapler': {
            'name': 'Stapler',
            'image': 'shop/images/product-stapler.png',
            'price': 100,
            'description': 'A practical stapler for school, home and office documents.',
            'features': [
                'Easy stapling mechanism',
                'Compact design',
                'Suitable for everyday office use',
            ],
        },
        'desk-organizer': {
            'name': 'Desk Organizer',
            'image': 'shop/images/office1.webp',
            'price': 120,
            'description': 'Keep stationery and desk essentials organized.',
            'features': [
                'Helps organize stationery',
                'Space-saving design',
                'Suitable for home and office',
            ],
        },
        'pen-set': {
            'name': 'Pen Set',
            'image': 'shop/images/product-pens.png',
            'price': 50,
            'description': 'A useful pen set for writing, studying and office work.',
            'features': [
                'For everyday writing',
                'Suitable for students',
                'Useful for office work',
            ],
        },
        'scissors': {
            'name': 'Scissors',
            'image': 'shop/images/product-scissors.png',
            'price': 60,
            'description': 'Scissors for common paper-cutting and stationery tasks.',
            'features': [
                'Useful for paper cutting',
                'Suitable for stationery tasks',
                'Practical everyday tool',
            ],
        },
        'office-supplies-set': {
            'name': 'Office Supplies Set',
            'image': 'shop/images/office2.jpeg',
            'price': 90,
            'description': 'A collection of stationery essentials for your workspace.',
            'features': [
                'Useful everyday supplies',
                'Suitable for study and office',
                'Keeps essentials together',
            ],
        },
        'highlighter-set': {
            'name': 'Highlighter Set',
            'image': 'shop/images/hero-highlighters.png',
            'price': 70,
            'description': 'Highlight important notes and study materials.',
            'features': [
                'Useful for revision',
                'Helps highlight important text',
                'Suitable for students and office work',
            ],
        },
        'desk-accessories': {
            'name': 'Desk Accessories',
            'image': 'shop/images/office3.jpeg',
            'price': 150,
            'description': 'Useful accessories for a neat and functional desk.',
            'features': [
                'Helps organize desk essentials',
                'Suitable for home and office',
                'Practical everyday accessories',
            ],
        },
        'notebook-set': {
            'name': 'Notebook Set',
            'image': 'shop/images/office4.jpeg',
            'price': 80,
            'description': 'A notebook set for notes, study and everyday writing.',
            'features': [
                'Useful for classes and meetings',
                'Suitable for daily note-taking',
                'Practical stationery essential',
            ],
        },
        'paper-stationery': {
            'name': 'Paper Stationery',
            'image': 'shop/images/paper1.jpeg',
            'price': 50,
            'description': 'Paper stationery essentials for everyday writing tasks.',
            'features': [
                'Useful for school and office',
                'Suitable for everyday tasks',
                'Essential paper stationery',
            ],
        },
        'notebook-accessories': {
            'name': 'Notebook Accessories',
            'image': 'shop/images/paper2.jpeg',
            'price': 110,
            'description': 'Accessories to support notebook organization and study.',
            'features': [
                'Useful for organizing notes',
                'Suitable for students',
                'Practical stationery accessories',
            ],
        },
        'writing-paper-set': {
            'name': 'Writing and Paper Set',
            'image': 'shop/images/paper3.jpeg',
            'price': 130,
            'description': 'A practical writing and paper set for school and office.',
            'features': [
                'Useful for writing activities',
                'Suitable for study and office work',
                'Everyday stationery essentials',
            ],
        },
                'file-folder': {
            'name': 'File Folder',
            'image': 'shop/images/files1.jpeg',
            'price': 80,
            'description': 'A practical file folder for organizing important documents.',
            'features': ['Easy document storage', 'Lightweight design', 'Suitable for office and school'],
        },
        'document-folder': {
            'name': 'Document Folder',
            'image': 'shop/images/files2.jpeg',
            'price': 120,
            'description': 'Keep your important documents organized in one folder.',
            'features': ['Organizes documents', 'Useful for office work', 'Easy to carry'],
        },
        'plastic-file': {
            'name': 'Plastic File',
            'image': 'shop/images/files3.jpeg',
            'price': 60,
            'description': 'A lightweight plastic file for everyday document storage.',
            'features': ['Lightweight material', 'Easy document storage', 'Suitable for daily use'],
        },
        'ring-binder': {
            'name': 'Ring Binder',
            'image': 'shop/images/files4.jpeg',
            'price': 150,
            'description': 'A ring binder for keeping papers neatly arranged.',
            'features': ['Keeps papers organized', 'Convenient document storage', 'Suitable for office use'],
        },
        'office-file': {
            'name': 'Office File',
            'image': 'shop/images/files5.jpeg',
            'price': 90,
            'description': 'An everyday office file for storing important paperwork.',
            'features': ['Organizes office documents', 'Easy to use', 'Suitable for daily office work'],
        },
        'expanding-file': {
            'name': 'Expanding File',
            'image': 'shop/images/files6.jpeg',
            'price': 200,
            'description': 'An expanding file for storing documents in separate sections.',
            'features': ['Multiple document sections', 'Helps organize paperwork', 'Useful for office and personal use'],
        },
        'button-file': {
            'name': 'Button File',
            'image': 'shop/images/files7.jpeg',
            'price': 50,
            'description': 'A simple button file for carrying papers securely.',
            'features': ['Button closure', 'Lightweight design', 'Easy to carry'],
        },
        'clear-folder': {
            'name': 'Clear Folder',
            'image': 'shop/images/files8.jpeg',
            'price': 100,
            'description': 'A clear folder for storing and viewing documents conveniently.',
            'features': ['Clear document visibility', 'Neat storage', 'Suitable for school and office'],
        },
        'project-file': {
            'name': 'Project File',
            'image': 'shop/images/files9.jpeg',
            'price': 180,
            'description': 'A project file for arranging assignments and project documents.',
            'features': ['Suitable for projects', 'Keeps pages organized', 'Useful for students'],
        },
        'lever-arch-file': {
            'name': 'Lever Arch File',
            'image': 'shop/images/files10.jpeg',
            'price': 250,
            'description': 'A lever arch file for organizing larger sets of paperwork.',
            'features': ['Stores multiple documents', 'Keeps paperwork organized', 'Suitable for office use'],
        },
        'document-organizer': {
            'name': 'Document Organizer',
            'image': 'shop/images/files11.jpeg',
            'price': 300,
            'description': 'A document organizer for keeping important papers together.',
            'features': ['Organized document storage', 'Useful for office paperwork', 'Helps keep documents together'],
        },
        'file-collection': {
            'name': 'File Collection',
            'image': 'shop/images/files12.jpeg',
            'price': 350,
            'description': 'A collection of files for different document storage needs.',
            'features': ['Useful for organizing documents', 'Suitable for school and office', 'Multiple filing options'],
        },
                'notebook': {
            'name': 'Notebook',
            'image': 'shop/images/paper1.jpeg',
            'price': 100,
            'description': 'A notebook for everyday writing, studying and note-taking.',
            'features': [
                'Suitable for daily writing',
                'Useful for students and office work',
                'Easy to carry',
            ],
        },
        'paper-notebook': {
            'name': 'Paper Notebook',
            'image': 'shop/images/paper2.jpeg',
            'price': 70,
            'description': 'A practical paper notebook for everyday notes.',
            'features': [
                'Useful for school and office',
                'Suitable for note-taking',
                'Convenient everyday stationery',
            ],
        },
        'drawing-paper': {
            'name': 'Drawing Paper',
            'image': 'shop/images/paper3.jpeg',
            'price': 140,
            'description': 'Drawing paper for creative work and art activities.',
            'features': [
                'Suitable for drawing',
                'Useful for creative projects',
                'Ideal for art activities',
            ],
        },
        'planner-notebook': {
            'name': 'Planner Notebook',
            'image': 'shop/images/paper4.jpeg',
            'price': 240,
            'description': 'A planner notebook for organizing schedules and tasks.',
            'features': [
                'Plan daily activities',
                'Organize tasks and notes',
                'Useful for study and work',
            ],
        },
        'writing-notebook': {
            'name': 'Writing Notebook',
            'image': 'shop/images/paper5.jpeg',
            'price': 270,
            'description': 'A notebook designed for writing and keeping notes.',
            'features': [
                'Suitable for regular writing',
                'Useful for notes and assignments',
                'Ideal for study and office',
            ],
        },
        'office-notebook': {
            'name': 'Office Notebook',
            'image': 'shop/images/paper6.jpeg',
            'price': 180,
            'description': 'An office notebook for meetings, planning and daily work.',
            'features': [
                'Useful for meeting notes',
                'Suitable for office tasks',
                'Helps organize information',
            ],
        },
        'notebook-set-paper': {
            'name': 'Notebook Set',
            'image': 'shop/images/paper7.webp',
            'price': 120,
            'description': 'A notebook set for study and everyday writing.',
            'features': [
                'Useful for school and college',
                'Suitable for daily notes',
                'Practical stationery set',
            ],
        },
        'study-notebook': {
            'name': 'Study Notebook',
            'image': 'shop/images/paper8.jpeg',
            'price': 90,
            'description': 'A study notebook for class notes and revision.',
            'features': [
                'Useful for class notes',
                'Suitable for revision',
                'Helps organize study material',
            ],
        },
        'premium-notebook': {
            'name': 'Premium Notebook',
            'image': 'shop/images/paper9.jpg',
            'price': 80,
            'description': 'A premium notebook for writing and note-taking.',
            'features': [
                'Suitable for everyday writing',
                'Useful for personal notes',
                'Practical stationery choice',
            ],
        },
        'paper-collection': {
            'name': 'Paper Collection',
            'image': 'shop/images/paper10.jpeg',
            'price': 150,
            'description': 'A collection of paper stationery for everyday tasks.',
            'features': [
                'Useful for school and office',
                'Suitable for paper-based activities',
                'Convenient stationery collection',
            ],
        },
        'creative-paper': {
            'name': 'Creative Paper',
            'image': 'shop/images/paper11.jpg',
            'price': 180,
            'description': 'Creative paper for art, craft and project activities.',
            'features': [
                'Suitable for creative projects',
                'Useful for arts and crafts',
                'Ideal for school activities',
            ],
        },
        'notebook-collection': {
            'name': 'Notebook Collection',
            'image': 'shop/images/paper12.jpg',
            'price': 230,
            'description': 'A notebook collection for different writing needs.',
            'features': [
                'Useful for multiple subjects',
                'Suitable for study and work',
                'Helps organize notes',
            ],
        },
                'blue-pen': {
            'name': 'Blue Pen',
            'image': 'shop/images/pen1.jpeg',
            'price': 90,
            'description': 'A blue pen for everyday writing at school, home and office.',
            'features': [
                'Suitable for everyday writing',
                'Useful for students and office work',
                'Practical stationery essential',
            ],
        },
        'ball-pen': {
            'name': 'Ball Pen',
            'image': 'shop/images/pen2.jpeg',
            'price': 70,
            'description': 'A ball pen for smooth everyday writing.',
            'features': [
                'Suitable for daily writing',
                'Useful for school and office',
                'Easy to carry',
            ],
        },
        'color-pen': {
            'name': 'Color Pen',
            'image': 'shop/images/pen3.jpeg',
            'price': 80,
            'description': 'Color pens for creative writing, drawing and note decoration.',
            'features': [
                'Useful for creative activities',
                'Suitable for notes and drawings',
                'Ideal for students',
            ],
        },
        'gel-pen': {
            'name': 'Gel Pen',
            'image': 'shop/images/pen4.jpeg',
            'price': 90,
            'description': 'A gel pen for everyday writing and note-taking.',
            'features': [
                'Suitable for writing notes',
                'Useful for study and office',
                'Practical writing tool',
            ],
        },
        'writing-pen': {
            'name': 'Writing Pen',
            'image': 'shop/images/pen5.jpeg',
            'price': 60,
            'description': 'A writing pen for schoolwork and daily use.',
            'features': [
                'Suitable for everyday writing',
                'Useful for assignments',
                'Convenient to carry',
            ],
        },
        'premium-pen': {
            'name': 'Premium Pen',
            'image': 'shop/images/pen6.jpeg',
            'price': 200,
            'description': 'A premium pen for writing at work, school or home.',
            'features': [
                'Suitable for regular writing',
                'Useful for meetings and notes',
                'Premium stationery option',
            ],
        },
        'pen-set-writing': {
            'name': 'Pen Set',
            'image': 'shop/images/pen7.jpeg',
            'price': 80,
            'description': 'A pen set for everyday writing and study needs.',
            'features': [
                'Useful for school and office',
                'Suitable for note-taking',
                'Practical stationery set',
            ],
        },
        'sketch-pen': {
            'name': 'Sketch Pen',
            'image': 'shop/images/pen8.jpeg',
            'price': 70,
            'description': 'Sketch pens for drawing, coloring and creative projects.',
            'features': [
                'Useful for drawing and coloring',
                'Suitable for creative projects',
                'Ideal for school activities',
            ],
        },
        'multicolor-pen': {
            'name': 'Multicolor Pen',
            'image': 'shop/images/pen9.jpeg',
            'price': 150,
            'description': 'A multicolor pen for organizing notes and highlighting information.',
            'features': [
                'Useful for color-coded notes',
                'Suitable for studying',
                'Helps organize written information',
            ],
        },
        'marker-pen': {
            'name': 'Marker Pen',
            'image': 'shop/images/pen10.jpeg',
            'price': 90,
            'description': 'A marker pen for writing, labeling and highlighting.',
            'features': [
                'Useful for labeling',
                'Suitable for office and school',
                'Practical writing accessory',
            ],
        },
        'fine-tip-pen': {
            'name': 'Fine Tip Pen',
            'image': 'shop/images/pen11.jpeg',
            'price': 120,
            'description': 'A fine tip pen for detailed writing and neat notes.',
            'features': [
                'Suitable for detailed writing',
                'Useful for notes and drawing',
                'Practical stationery tool',
            ],
        },
        'pen-collection': {
            'name': 'Pen Collection',
            'image': 'shop/images/pen12.jpeg',
            'price': 100,
            'description': 'A pen collection for everyday writing and stationery needs.',
            'features': [
                'Useful for study and office',
                'Suitable for everyday writing',
                'Convenient stationery collection',
            ],
        },
                'school-supplies-set': {
            'name': 'School Supplies Set',
            'image': 'shop/images/school1.jpeg',
            'price': 50,
            'description': 'A stationery set for everyday school activities.',
            'features': [
                'Useful for schoolwork',
                'Suitable for students',
                'Everyday stationery essentials',
            ],
        },
        'school-stationery': {
            'name': 'School Stationery',
            'image': 'shop/images/school2.jpeg',
            'price': 120,
            'description': 'Essential stationery items for school and classroom use.',
            'features': [
                'Useful for daily schoolwork',
                'Suitable for students',
                'Practical stationery items',
            ],
        },
        'student-stationery': {
            'name': 'Student Stationery',
            'image': 'shop/images/school3.jpeg',
            'price': 250,
            'description': 'Stationery essentials to support students with their studies.',
            'features': [
                'Useful for assignments',
                'Suitable for school and college',
                'Helps with everyday study tasks',
            ],
        },
        'school-kit': {
            'name': 'School Kit',
            'image': 'shop/images/school4.jpeg',
            'price': 350,
            'description': 'A school kit for students and their everyday learning needs.',
            'features': [
                'Useful for classroom activities',
                'Suitable for students',
                'Convenient school essentials',
            ],
        },
        'student-kit': {
            'name': 'Student Kit',
            'image': 'shop/images/school5.jpeg',
            'price': 80,
            'description': 'A practical kit for everyday student stationery needs.',
            'features': [
                'Useful for schoolwork',
                'Easy to carry',
                'Suitable for daily study',
            ],
        },
        'school-essentials': {
            'name': 'School Essentials',
            'image': 'shop/images/school6.jpeg',
            'price': 180,
            'description': 'School essentials for learning and classroom activities.',
            'features': [
                'Useful for everyday learning',
                'Suitable for classroom use',
                'Practical student supplies',
            ],
        },
        'writing-supplies': {
            'name': 'Writing Supplies',
            'image': 'shop/images/school7.jpeg',
            'price': 220,
            'description': 'Writing supplies for notes, assignments and schoolwork.',
            'features': [
                'Useful for writing tasks',
                'Suitable for students',
                'Supports everyday schoolwork',
            ],
        },
        'school-accessories': {
            'name': 'School Accessories',
            'image': 'shop/images/school8.jpeg',
            'price': 450,
            'description': 'School accessories for students and classroom activities.',
            'features': [
                'Useful for school routines',
                'Suitable for students',
                'Practical school accessories',
            ],
        },
        'learning-supplies': {
            'name': 'Learning Supplies',
            'image': 'shop/images/school9.jpeg',
            'price': 95,
            'description': 'Learning supplies to support everyday educational activities.',
            'features': [
                'Useful for study sessions',
                'Suitable for students',
                'Supports learning activities',
            ],
        },
        'classroom-supplies': {
            'name': 'Classroom Supplies',
            'image': 'shop/images/school10.jpeg',
            'price': 150,
            'description': 'Supplies for classroom activities and everyday learning.',
            'features': [
                'Useful for classroom tasks',
                'Suitable for school use',
                'Practical learning essentials',
            ],
        },
        'study-materials': {
            'name': 'Study Materials',
            'image': 'shop/images/school11.jpeg',
            'price': 300,
            'description': 'Study materials for schoolwork, revision and learning.',
            'features': [
                'Useful for revision',
                'Suitable for students',
                'Supports study activities',
            ],
        },
        'school-collection': {
            'name': 'School Collection',
            'image': 'shop/images/school12.jpeg',
            'price': 400,
            'description': 'A collection of school supplies for everyday educational needs.',
            'features': [
                'Useful for school activities',
                'Suitable for students',
                'A practical stationery collection',
            ],
        },
    }

    product = products.get(product_slug)

    if product is None:
        from django.http import Http404
        raise Http404("Product not found")

    return render(
        request,
        'shop/product_details.html',
        {'product': product}
    )

def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        message = request.POST.get('message', '').strip()

        if name and email and phone and message:
            messages.success(
                request,
                'Thank you! Your message has been submitted successfully.',
                fail_silently=False
            )
            return redirect('contact')
        else:
            messages.error(request, 'Please fill in all fields.')

    return render(request, 'shop/contact.html')



def login_page(request):
    if request.method == 'POST':
        auth_mode = request.POST.get('auth_mode', 'login')
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')

        if auth_mode == 'signup':
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            confirm_password = request.POST.get(
                'confirm_password', ''
            )

            if not name or not email or not phone or not password:
                messages.error(request, 'Please fill in all fields.')

            elif password != confirm_password:
                messages.error(request, 'Passwords do not match.')

            elif User.objects.filter(email__iexact=email).exists():
                messages.error(
                    request,
                    'This email is already registered. Please sign in.'
                )

            else:
                user = User.objects.create_user(
                    username=email,
                    email=email,
                    password=password,
                    first_name=name
                )

                UserProfile.objects.create(
                    user=user,
                    phone=phone
                )

                authenticated_user = authenticate(
                    request,
                    username=user.username,
                    password=password
                )

                if authenticated_user is not None:
                    login(request, authenticated_user)
                    messages.success(
                        request,
                        'Registration successful! Welcome to Supplyhive.'
                    )
                    request.session['login_success_redirect'] = 'my_orders'
                    return redirect('login')

                messages.success(
                    request,
                    'Registration successful! Please sign in.'
                )

        else:
            existing_user = User.objects.filter(
                email__iexact=email
            ).first()

            if existing_user is None:
                messages.error(
                    request,
                    'Account not found. Please sign up first.'
                )

            else:
                user = authenticate(
                    request,
                    username=existing_user.username,
                    password=password
                )

                if user is not None:
                    login(request, user)

                    next_url = request.GET.get(
                        'next',
                        request.POST.get('next', '')
                    )

                    if next_url == '/checkout/':
                        request.session['login_success_redirect'] = 'checkout'
                    else:
                        request.session['login_success_redirect'] = 'my_orders'

                    messages.success(
                        request,
                        'Login successful! Welcome to Supplyhive.'
                    )
                    return redirect('login')

                else:
                    messages.error(
                        request,
                        'Incorrect password. Please try again.'
                    )

    if request.user.is_authenticated:
        redirect_to = request.session.pop(
            'login_success_redirect', None
        )

        if redirect_to:
            return render(
                request,
                'shop/login.html',
                {'redirect_to': redirect_to}
            )

    return render(request, 'shop/login.html')


def files_folders(request):
    query = request.GET.get('q', '').strip()

    products = [
        {'name': 'File Folder', 'slug': 'file-folder', 'image': 'shop/images/files1.jpeg', 'price': 80},
        {'name': 'Document Folder', 'slug': 'document-folder', 'image': 'shop/images/files2.jpeg', 'price': 120},
        {'name': 'Plastic File', 'slug': 'plastic-file', 'image': 'shop/images/files3.jpeg', 'price': 60},
        {'name': 'Ring Binder', 'slug': 'ring-binder', 'image': 'shop/images/files4.jpeg', 'price': 150},
        {'name': 'Office File', 'slug': 'office-file', 'image': 'shop/images/files5.jpeg', 'price': 90},
        {'name': 'Expanding File', 'slug': 'expanding-file', 'image': 'shop/images/files6.jpeg', 'price': 200},
        {'name': 'Button File', 'slug': 'button-file', 'image': 'shop/images/files7.jpeg', 'price': 50},
        {'name': 'Clear Folder', 'slug': 'clear-folder', 'image': 'shop/images/files8.jpeg', 'price': 100},
        {'name': 'Project File', 'slug': 'project-file', 'image': 'shop/images/files9.jpeg', 'price': 180},
        {'name': 'Lever Arch File', 'slug': 'lever-arch-file', 'image': 'shop/images/files10.jpeg', 'price': 250},
        {'name': 'Document Organizer', 'slug': 'document-organizer', 'image': 'shop/images/files11.jpeg', 'price': 300},
        {'name': 'File Collection', 'slug': 'file-collection', 'image': 'shop/images/files12.jpeg', 'price': 350},
    ]

    if query:
        search_text = ''.join(query.casefold().split())
        products = [
            product for product in products
            if search_text in ''.join(product['name'].casefold().split())
        ]

    return render(
        request,
        'shop/files_folders.html',
        {
            'products': products,
            'search_query': query,
        }
    )



def paper_notebooks(request):
    return render(request, 'shop/paper_notebooks.html')


def pens_writing(request):
    return render(request, 'shop/pens_writing.html')


def school_supplies(request):
    return render(request, 'shop/school_supplies.html')


def cart(request):
    return render(request, 'shop/cart.html')


def checkout(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/checkout/')

    # Show login success popup only after successful login
    show_login_success = request.session.pop(
        'show_login_success', False
    )

    if request.method == 'POST':
        full_name = request.POST.get('full_name', '').strip()
        phone = request.POST.get('phone', '').strip()
        email = request.POST.get('email', '').strip()
        address = request.POST.get('address', '').strip()
        city = request.POST.get('city', '').strip()
        state = request.POST.get(
            'state', 'Tamil Nadu'
        ).strip()
        pincode = request.POST.get('pincode', '').strip()

        # Identify Buy Now checkout
        buy_now = request.POST.get('buy_now') == 'true'
        buy_now_product = request.POST.get(
            'buy_now_product', ''
        )

        if not all([
            full_name,
            phone,
            email,
            address,
            city,
            state,
            pincode
        ]):
            messages.error(
                request,
                'Please fill in all delivery details.'
            )

        elif not pincode.isdigit() or len(pincode) != 6:
            messages.error(
                request,
                'Enter a valid 6-digit pincode.'
            )

        else:
            # Save delivery details
            CheckoutDetails.objects.create(
                user=request.user,
                full_name=full_name,
                phone=phone,
                email=email,
                address=address,
                city=city,
                state=state,
                pincode=pincode
            )

            # Save Buy Now product for the payment step
            if buy_now:
                try:
                    selected_product = json.loads(
                        buy_now_product
                    )

                    if (
                        not isinstance(selected_product, list)
                        or len(selected_product) != 1
                        or not isinstance(
                            selected_product[0], dict
                        )
                    ):
                        messages.error(
                            request,
                            'Invalid Buy Now product.'
                        )
                        return redirect('cart')

                    request.session['buy_now_product'] = (
                        selected_product
                    )

                except (json.JSONDecodeError, TypeError):
                    messages.error(
                        request,
                        'Invalid Buy Now product.'
                    )
                    return redirect('cart')

            else:
                # Normal Add to Cart checkout
                request.session.pop(
                    'buy_now_product', None
                )

            request.session.pop('payment_method', None)
            return redirect('payment_details')

    return render(
        request,
        'shop/checkout.html',
        {
            'show_login_success': show_login_success
        }
    )


def payment(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/checkout/')

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', '')

        if payment_method not in ['CARD', 'UPI', 'NETBANKING', 'COD']:
            messages.error(
                request,
                'Please select a valid payment method.'
            )
            return redirect('payment')

        request.session['payment_method'] = payment_method
        return redirect('payment_details')

    return render(request, 'shop/payment.html')


def payment_details(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/checkout/')

    payment_method = request.session.get('payment_method')

    if request.method == 'POST':
        payment_method = (
            request.POST.get('payment_method')
            or payment_method
        )

        if payment_method not in [
            'CARD', 'UPI', 'NETBANKING', 'COD'
        ]:
            messages.error(
                request,
                'Please select a valid payment method.'
            )
            return redirect('payment_details')

        # Validate demo payment details
        if payment_method == 'CARD':
            card_name = request.POST.get(
                'card_name', ''
            ).strip()
            card_number = request.POST.get(
                'card_number', ''
            ).replace(' ', '')
            expiry = request.POST.get(
                'expiry', ''
            ).strip()
            cvv = request.POST.get('cvv', '').strip()

            if not card_name:
                messages.error(
                    request, 'Enter the name on card.'
                )
                return redirect('payment_details')

            if (
                not card_number.isdigit()
                or len(card_number) != 16
            ):
                messages.error(
                    request,
                    'Card number must contain 16 digits.'
                )
                return redirect('payment_details')

            if (
                len(expiry) != 5
                or expiry[2] != '/'
                or not expiry[:2].isdigit()
                or not expiry[3:].isdigit()
                or not 1 <= int(expiry[:2]) <= 12
            ):
                messages.error(
                    request,
                    'Enter a valid expiry date in MM/YY format.'
                )
                return redirect('payment_details')

            if not cvv.isdigit() or len(cvv) not in [3, 4]:
                messages.error(
                    request,
                    'Enter a valid 3 or 4 digit CVV.'
                )
                return redirect('payment_details')

        elif payment_method == 'UPI':
            upi_id = request.POST.get(
                'upi_id', ''
            ).strip()

            if '@' not in upi_id or ' ' in upi_id:
                messages.error(
                    request,
                    'Enter a valid UPI ID format.'
                )
                return redirect('payment_details')

        elif payment_method == 'NETBANKING':
            bank_name = request.POST.get(
                'bank_name', ''
            ).strip()

            if not bank_name:
                messages.error(
                    request,
                    'Please select your bank.'
                )
                return redirect('payment_details')

        # Buy Now uses the server-side session product.
        # Normal checkout uses cart_data from the payment form.
        buy_now_items = request.session.get(
            'buy_now_product'
        )

        if buy_now_items:
            cart_items = buy_now_items
        else:
            cart_json = request.POST.get('cart_data', '')

            try:
                cart_items = json.loads(cart_json)
            except (json.JSONDecodeError, TypeError):
                cart_items = None

        if not isinstance(cart_items, list) or not cart_items:
            messages.error(
                request,
                'Your cart is empty or cart details are missing. '
                'Please return to your cart and try again.'
            )
            return redirect('cart')

        # Get delivery details saved during checkout
        checkout_details = CheckoutDetails.objects.filter(
            user=request.user
        ).order_by('-created_at').first()

        if checkout_details is None:
            messages.error(
                request,
                'Please submit your delivery details first.'
            )
            return redirect('checkout')

        # Validate items and calculate total
        validated_items = []
        total_amount = Decimal('0.00')

        try:
            for item in cart_items:
                if not isinstance(item, dict):
                    raise ValueError('Invalid cart item.')

                name = str(item.get('name', '')).strip()
                image = str(item.get('image', '')).strip()
                quantity = int(item.get('quantity', 0))
                price = Decimal(str(item.get('price', '0')))

                if (
                    not name
                    or quantity < 1
                    or quantity > 1000
                    or not price.is_finite()
                    or price < 0
                    or price > Decimal('10000000')
                ):
                    raise ValueError('Invalid product details.')

                price = price.quantize(Decimal('0.01'))
                item_total = (
                    price * quantity
                ).quantize(Decimal('0.01'))

                validated_items.append({
                    'name': name,
                    'image': image,
                    'quantity': quantity,
                    'price': price,
                    'item_total': item_total,
                })

                total_amount += item_total

        except (ValueError, TypeError, InvalidOperation):
            messages.error(
                request,
                'Invalid cart details. Please check your cart.'
            )
            return redirect('cart')

        method_names = {
            'CARD': 'Card Demo Payment',
            'UPI': 'UPI Demo Payment',
            'NETBANKING': 'Net Banking Demo Payment',
            'COD': 'Cash on Delivery',
        }

        # Demo payment only; no real payment is processed.
        payment_status = 'PENDING'

        # Create order and items together
        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                payment_method=payment_method,
                payment_status=payment_status,
                total_amount=total_amount,
            )

            for item in validated_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item['name'],
                    product_image=item['image'],
                    quantity=item['quantity'],
                    unit_price=item['price'],
                    item_total=item['item_total'],
                )

        # Clear Buy Now session after successful order creation
        request.session.pop('buy_now_product', None)

        request.session['last_order_id'] = order.order_id
        request.session['demo_payment_success'] = (
            payment_method != 'COD'
        )

        context = {
            'order': order,
            'order_id': order.order_id,
            'payment_method': method_names[payment_method],
            'payment_status': order.payment_status,
            'demo_payment': payment_method != 'COD',
            'order_date': order.created_at,
            'cart_items': [
                {
                    'name': item['name'],
                    'image': item['image'],
                    'quantity': item['quantity'],
                    'price': item['price'],
                    'total': item['item_total'],
                }
                for item in validated_items
            ],
            'subtotal': total_amount,
            'shipping': Decimal('0.00'),
            'total_amount': total_amount,
            'checkout_details': checkout_details,
        }

        return render(
            request,
            'shop/order_success.html',
            context
        )

    return render(
        request,
        'shop/payment_details.html',
        {'payment_method': payment_method}
    )


@login_required
def bill_download(request, order_id):
    # Get the order belonging to the logged-in user
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    # Get the latest delivery address saved during checkout
    checkout_details = CheckoutDetails.objects.filter(
        user=request.user
    ).order_by('-id').first()

    # Create PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = (
        f'attachment; filename="Supplyhive_Bill_{order.order_id}.pdf"'
    )

    # Build PDF
    pdf = SimpleDocTemplate(
        response,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()
    elements = []

    # Bill heading
    elements.append(
        Paragraph("<b>SUPPLYHIVE</b>", styles['Title'])
    )
    elements.append(
        Paragraph("Order Invoice / Bill", styles['Heading2'])
    )
    elements.append(Spacer(1, 15))

    # Order information
    elements.append(
        Paragraph(
            f"<b>Order ID:</b> {order.order_id}",
            styles['Normal']
        )
    )
    elements.append(
        Paragraph(
            f"<b>Order Date:</b> "
            f"{order.created_at.strftime('%d-%m-%Y %I:%M %p')}",
            styles['Normal']
        )
    )
    elements.append(Spacer(1, 15))

    # Customer information
    elements.append(
        Paragraph("<b>Customer Details</b>", styles['Heading2'])
    )

    if checkout_details:
        customer_lines = [
            f"Name: {checkout_details.full_name}",
            f"Phone: {checkout_details.phone}",
            f"Email: {checkout_details.email}",
            f"Address: {checkout_details.address}",
            f"City: {checkout_details.city}",
            f"State: {checkout_details.state}",
            f"Pincode: {checkout_details.pincode}",
        ]

        for line in customer_lines:
            elements.append(Paragraph(line, styles['Normal']))
    else:
        elements.append(
            Paragraph(
                f"Customer: {request.user.username}",
                styles['Normal']
            )
        )

    elements.append(Spacer(1, 20))

    # Product table
    elements.append(
        Paragraph("<b>Order Summary</b>", styles['Heading2'])
    )

    table_data = [
        ['Product', 'Qty', 'Unit Price', 'Amount']
    ]

    for item in order.items.all():
        table_data.append([
            item.product_name,
            str(item.quantity),
            f"Rs. {item.unit_price:.2f}",
            f"Rs. {item.item_total:.2f}",
        ])

    table_data.append([
        '', '', 'Total Amount',
        f"Rs. {order.total_amount:.2f}"
    ])

    bill_table = Table(
        table_data,
        colWidths=[210, 45, 100, 100],
        repeatRows=1
    )

    bill_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#2463EB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#EAF1FF')),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
    ]))

    elements.append(bill_table)
    elements.append(Spacer(1, 20))

    # Payment information
    elements.append(
        Paragraph("<b>Payment Details</b>", styles['Heading2'])
    )
    elements.append(
        Paragraph(
            f"Payment Method: {order.get_payment_method_display()}",
            styles['Normal']
        )
    )
    elements.append(
        Paragraph(
            f"Payment Status: {order.payment_status}",
            styles['Normal']
        )
    )

    elements.append(Spacer(1, 25))
    elements.append(
        Paragraph(
            "Thank you for shopping with Supplyhive!",
            styles['Normal']
        )
    )
    elements.append(
        Paragraph(
            "This bill was generated by the Supplyhive demo website.",
            styles['Italic']
        )
    )

    pdf.build(elements)

    return response


def my_orders(request):
    if not request.user.is_authenticated:
        return redirect('/login/?next=/my-orders/')

    orders = (
        Order.objects
        .filter(user=request.user)
        .prefetch_related('items')
        .order_by('-created_at')
    )

    return render(
        request,
        'shop/my_orders.html',
        {'orders': orders}
    )

@login_required
def order_tracking(request, order_id):
    order = get_object_or_404(
        Order,
        id=order_id,
        user=request.user
    )

    return render(
        request,
        'shop/order_tracking.html',
        {'order': order}
    )


def logout_page(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')

    return redirect('home')


@login_required
def my_addresses(request):
    addresses = (
        CheckoutDetails.objects
        .filter(user=request.user)
        .order_by('-created_at')
    )

    return render(
        request,
        'shop/my_addresses.html',
        {'addresses': addresses}
    )

@login_required
def edit_address(request, address_id):
    address = get_object_or_404(
        CheckoutDetails,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        address.full_name = request.POST.get('full_name', '').strip()
        address.phone = request.POST.get('phone', '').strip()
        address.email = request.POST.get('email', '').strip()
        address.address = request.POST.get('address', '').strip()
        address.city = request.POST.get('city', '').strip()
        address.state = request.POST.get('state', '').strip()
        address.pincode = request.POST.get('pincode', '').strip()

        address.save()
        messages.success(request, 'Address updated successfully!')
        return redirect('my_addresses')

    return render(
        request,
        'shop/edit_address.html',
        {'address': address}
    )


@login_required
def delete_address(request, address_id):
    address = get_object_or_404(
        CheckoutDetails,
        id=address_id,
        user=request.user
    )

    if request.method == 'POST':
        address.delete()
        messages.success(request, 'Address deleted successfully!')

    return redirect('my_addresses')
@login_required
def my_account(request):
    return render(request, 'shop/my_account.html')