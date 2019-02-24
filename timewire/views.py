from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.urls import reverse
from django.contrib import messages
from .models import Work
from django.views import generic
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.utils import timezone

from .forms import LoginForm, RegisterForm, PostForm

# Create your views here.

# ユーザー登録＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
class RegisterView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(reverse('timewire:index'))
        context = {
            'form': RegisterForm(),
        }
        return render(request, 'register.html', context)

    def post(self, request, *args, **kwargs):
       form = RegisterForm(request.POST)
       if not form.is_valid():
           return render(request, 'register.html', {'form': form})
       user = form.save(commit=False)
       user.set_password(form.cleaned_data['password'])
       user.save()
       auth_login(request, user)
       messages.info(request, "登録が完了し、自動ログインしました。")
       return redirect(reverse('timewire:index'))


register = RegisterView.as_view()

# ログイン画面＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
class LoginView(View):
    def get(self, request, *args, **kwargs):
        context = {
            'form': LoginForm(),
        }
        return render(request, 'login.html', context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        # バリデーションNGの場合
        if not form.is_valid():
            messages.error(request, "ログインに失敗しました")
            return render(request, 'login.html', {'form':form})
        # バリデーションOKの場合
        # user = form.get_user()
        email = request.POST['email']
        password = request.POST['password']
        # 認証
        user = authenticate(email=email,password=password)
        # ログイン処理
        auth_login(request, user)

        messages.info(request, "ログインしました。")

        return redirect(reverse('timewire:index'))
                                    # app:name


login = LoginView.as_view()

# ログアウト＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class LogoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            auth_logout(request)
        messages.info(request, "ログアウトしました")
        return redirect(reverse('timewire:login'))


logout = LogoutView.as_view()

# ベースビュー＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class BaseView(View):
    def get(self, request, *args, **kwargs):

        return render(request, 'base.html',)

    def post(self, request, *args, **kwargs):

        return render(request, 'base.html',)


base = BaseView.as_view()

# 投稿一覧＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
class IndexView(View):
    def get(self, request, *args, **kwargs):
        form = PostForm()
        return render(request, 'index.html', {'works': Work.objects.all().order_by('-date'),'form': form})

    def post(self, request, *args, **kwargs):
        name = request.POST['name']
        price = request.POST['price']
        content = request.POST['content']
        work = Work(name=name, price=price, content=content)
        work.save()
        messages.info(request, "ワークの登録が完了しました。")
        return redirect(reverse('timewire:index'))
        #
        # return render(request, 'index.html')


index = IndexView.as_view()


# 投稿削除＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
# class DeleteView(View):
#     def delete(self, request, *args, **kwargs):
#         id = request.POST['id']
#         w = Work.objects.get(id=id)
#         print(w)
#         w.delete()
#         return redirect(reverse('timewire:index'))
#         # return HttpResponseRedirect(reverse('timewire:index'))
#
# delete = DeleteView.as_view()

class DeleteView(generic.edit.DeleteView):
    model = Work

    success_url = reverse_lazy('timewire:index')
    # template_name = 'timewire/index.html'

    def delete(self, request, *args, **kwargs):
        result = super().delete(request, *args, **kwargs)
        messages.info(
            self.request, 'ワークの削除が完了しました')
        return result


delete = DeleteView.as_view()
# url結びつけ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝