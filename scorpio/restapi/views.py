from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings

import os


def doc(request):
    ctx = {}

    return render(request, 'restapi/doc.html', ctx)


# def vue(vue_root):
#     for template in settings.TEMPLATES:
#         if template['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
#             template_dir = '%s/dist' % vue_root
#             if template_dir not in template['DIRS']:
#                 template['DIRS'].append(template_dir)

#     static_dir = os.path.join(settings.BASE_DIR, '%s/dist/static' % vue_root)
#     if static_dir not in settings.STATICFILES_DIRS:
#         settings.STATICFILES_DIRS.append(static_dir)

#     def vue_view(request):
#         return render(request, 'index.html')

#     return vue_view

def vue():
    def vue_view(request):
        return render(request, 'index.html')

    return vue_view
