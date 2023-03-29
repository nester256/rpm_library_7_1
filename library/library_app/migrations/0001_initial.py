# Generated by Django 4.1.7 on 2023-03-28 21:10

import datetime
from django.db import migrations, models
import django.db.models.deletion
import library_app.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='modified')),
                ('full_name', models.TextField(verbose_name='full name')),
            ],
            options={
                'verbose_name': 'author',
                'verbose_name_plural': 'authors',
                'db_table': 'author',
            },
        ),
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='modified')),
                ('title', models.CharField(max_length=40, verbose_name='title')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('volume', models.IntegerField(validators=[library_app.models.validate_volume], verbose_name='volume')),
                ('type', models.CharField(blank=True, choices=[('book', 'book'), ('magazine', 'magazine')], max_length=20, null=True, verbose_name='type')),
                ('year', models.IntegerField(blank=True, null=True, verbose_name='year')),
            ],
            options={
                'verbose_name': 'book',
                'verbose_name_plural': 'books',
                'db_table': 'book',
            },
        ),
        migrations.CreateModel(
            name='BookGenre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='created')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library_app.book')),
            ],
            options={
                'db_table': 'book_genre',
            },
        ),
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='created')),
                ('modified', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='modified')),
                ('name', models.CharField(choices=[('fantasy', 'fantasy'), ('fiction', 'fiction'), ('detective', 'detective')], max_length=30, verbose_name='name')),
                ('description', models.TextField(blank=True, null=True, verbose_name='description')),
                ('books', models.ManyToManyField(through='library_app.BookGenre', to='library_app.book', verbose_name='books')),
            ],
            options={
                'verbose_name': 'genre',
                'verbose_name_plural': 'genres',
                'db_table': 'genre',
            },
        ),
        migrations.AddField(
            model_name='bookgenre',
            name='genre',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library_app.genre'),
        ),
        migrations.CreateModel(
            name='BookAuthor',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(blank=True, default=datetime.datetime.now, verbose_name='created')),
                ('author', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library_app.author')),
                ('book', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='library_app.book')),
            ],
            options={
                'db_table': 'book_author',
                'unique_together': {('book', 'author')},
            },
        ),
        migrations.AddField(
            model_name='book',
            name='authors',
            field=models.ManyToManyField(through='library_app.BookAuthor', to='library_app.author', verbose_name='authors'),
        ),
        migrations.AddField(
            model_name='book',
            name='genres',
            field=models.ManyToManyField(through='library_app.BookGenre', to='library_app.genre', verbose_name='genres'),
        ),
        migrations.AddField(
            model_name='author',
            name='books',
            field=models.ManyToManyField(through='library_app.BookAuthor', to='library_app.book', verbose_name='books'),
        ),
        migrations.AlterUniqueTogether(
            name='bookgenre',
            unique_together={('book', 'genre')},
        ),
    ]