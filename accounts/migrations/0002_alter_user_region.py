# Generated by Django 3.2.18 on 2023-05-17 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='region',
            field=models.CharField(choices=[('서울', '서울'), ('인천', '인천'), ('부산', '부산'), ('울산', '울산'), ('대구', '대구'), ('광주', '광주'), ('대전', '대전'), ('세종특별자치시', '세종특별자치시'), ('제주특별자치도', '제주특별자치도'), ('경기', '경기'), ('강원', '강원'), ('충북', '충북'), ('충남', '충남'), ('전북', '전북'), ('전남', '전남'), ('경북', '경북'), ('경남', '경남')], default='서울', max_length=10),
        ),
    ]
