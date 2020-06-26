import json
from django.test import TestCase, Client
from django.urls import reverse
from budget.models import Project, Category, Expense

class TestViews(TestCase):

    def setUp(self):
        '''
        setup code
        '''
        self.client = Client()
        self.list_url = reverse('list')
        self.detail_url = reverse('detail', args=['project1'])
        self.list_template_name = 'budget/project-list.html'
        self.detail_template_name = 'budget/project-detail.html'
        self.project1 = Project.objects.create(
            name='project1',
            budget=1000
        )


    def test_project_list_GET(self):
        '''
        list view test
        '''
        response = self.client.get(self.list_url) # test code
        self.assertEquals(response.status_code, 200) # get ok
        self.assertTemplateUsed(response, self.list_template_name) # template test

    def test_project_detail_GET(self):
        '''
        detail view get test
        '''
        response = self.client.get(self.detail_url) # test code
        self.assertEquals(response.status_code, 200) # get ok
        self.assertTemplateUsed(response, self.detail_template_name) # template test

    def test_project_detail_POST_adds_new_expense(self):
        Category.objects.create(
            project= self.project1,
            name='development'
        )
        response = self.client.post(self.detail_url, {
            'title': 'expense1',
            'amount': 1000,
            'category': 'development'
        })
        self.assertEquals(response.status_code, 302) # created
        self.assertEquals(self.project1.expenses.first().title, 'expense1')

    def test_project_detail_POST_no_data(self):
        response = self.client.post(self.detail_url)
        self.assertEquals(response.status_code, 302) # created
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_delete_expense(self):
        category1 = Category.objects.create(
            project= self.project1,
            name='development'
        )
        Expense.objects.create(
            project = self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url, json.dumps({
            'id':1
        }))

        self.assertEquals(response.status_code, 204) # no content
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_no_id(self):
        category1 = Category.objects.create(
            project= self.project1,
            name='development'
        )
        Expense.objects.create(
            project = self.project1,
            title='expense1',
            amount=1000,
            category=category1
        )

        response = self.client.delete(self.detail_url)

        self.assertEquals(response.status_code, 404) # not found
        self.assertEquals(self.project1.expenses.count(), 1)

    def test_project_create_POST(self):
        url = reverse('add')
        response = self.client.post(url, {
            'name': 'project2',
            'budget': 10000,
            'categoriesString': 'design,development'
        })
        project2 = Project.objects.get(id=2)
        self.assertEquals(project2.name, 'project2')

        first_category = Category.objects.get(id=1)
        self.assertEquals(first_category.project, project2)
        self.assertEquals(first_category.name, 'design')

        second_category = Category.objects.get(id=2)
        self.assertEquals(second_category.project, project2)
        self.assertEquals(second_category.name, 'development')



