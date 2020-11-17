# Generated by Django 3.1.3 on 2020-11-17 20:37

import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='auth.user')),
                ('avatar', models.FilePathField()),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('content', models.TextField(verbose_name='content')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('rating', models.IntegerField(default=0, verbose_name='rating')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('tags', models.ManyToManyField(to='main.Tag')),
            ],
            options={
                'verbose_name': 'вопрос',
                'verbose_name_plural': 'вопросы',
            },
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(verbose_name='content')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation_date')),
                ('correct', models.BooleanField(default=False)),
                ('rating', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.question')),
            ],
            options={
                'verbose_name': 'ответ',
                'verbose_name_plural': 'ответы',
            },
        ),
        migrations.CreateModel(
            name='Question_Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('question', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.question')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
            options={
                'unique_together': {('question', 'user')},
            },
        ),
        migrations.CreateModel(
            name='Answer_Like',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.IntegerField(default=0)),
                ('answer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.answer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.profile')),
            ],
            options={
                'unique_together': {('answer', 'user')},
            },
        ),
    ]
