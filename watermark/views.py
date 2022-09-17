import os

from django.shortcuts import render, HttpResponse
from django.http import JsonResponse

# Create your views here.
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os


def test(request):
    if request.method == 'GET':
        return render(request, 'test.html')


def get_img(request):
    font = ImageFont.truetype(font='./static/font/1641263938811335.ttf', size=50)
    image = Image.open('./1.png')
    w, h = image.size
    print(w, h)
    draw = ImageDraw.Draw(image)
    draw.text((w / 2, h - 60), text='机密文件', fill=(255, 0, 0), font=font)
    byte_io = BytesIO()
    image.save(byte_io, format='png')
    return HttpResponse(byte_io.getvalue())


def index(request):
    if request.method == 'GET':
        import os
        list_dir = os.listdir('./media/img/')
        return render(request, 'index.html', context={'img_list': list_dir})


def handle(request):
    if request.method == 'POST':
        print(request.POST)
        text = request.POST.get('text')
        gx = request.POST.getlist('gx')
        print(gx)
        for i in gx:
            img = Image.open('./media/img/' + i)
            w, h = img.size
            font = ImageFont.truetype(font='./static/font/1641263938811335.ttf', size=h // 15)
            draw = ImageDraw.Draw(img)
            print(2)
            draw.text((0, h - h // 15 - 20), text=text, fill=(255, 0, 0), font=font)
            print(3)
            img.save(f'./media/handle/{i}', 'png')
        request.session['handle_list'] = gx
        return JsonResponse('ok', safe=False)
    else:
        handle_list = request.session.get('handle_list')
        print(handle_list)
        return render(request, 'handle.html', context={'handle_list': handle_list})


def add_img(request):
    res = {'code': 100, 'mag': '添加成功'}
    try:
        img = request.FILES.get('img')
        name = request.POST.get('name')
        img = Image.open(img)
        img.save(os.path.join('./media/img/', name), 'png')
        return JsonResponse(res)
    except Exception:
        res['code'] = 101
        res['msg'] = '添加失败'
        return JsonResponse(res)


def del_img(request):
    gx = request.POST.getlist('gx')
    for i in gx:
        os.remove(os.path.join('./media/img/', i))
        os.remove(os.path.join('./media/handle/', i))
    return JsonResponse('ok', safe=False)
