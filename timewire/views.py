from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
from django.urls import reverse
from django.contrib import messages
from .models import Work, User
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

# マイページ＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
class MyPageView(View):
    def get(self,request):
        return render(request, 'myPage.html',)

myPage = MyPageView.as_view()

# プロフィール＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
class ProfileView(View):
    def get(self,request, user_id):
        user = User.objects.get(pk=user_id)
        context = {
            'user': user
        }
        return render(request, 'profile.html', context)

profile = ProfileView.as_view()

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
        works = Work.objects.all().order_by('-date')
        form = PostForm()
        context = {
            'works': works,
            'form': form,
        }
        return render(request, 'index.html', context)

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

# 投稿詳細＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝
#


class DetailView(View):
    def get(self, request, work_id):
        work = Work.objects.get(pk=work_id)
        form = PostForm()
        context = {
            'form': form,
            'work': work,
        }
        return render(request, 'detail.html', context)


        # return render(request, 'detail.html')
        #
        # work = Work.objects.get(work_id=id)
        # context = {'work': work}
        # form = PostForm()
        # return render(request, 'detail.html', {'form': form},context)


detail = DetailView.as_view()




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

# 以下サイト参照
# https://tech.torico-corp.com/blog/django-crud-generic-view/

delete = DeleteView.as_view()

# 投稿更新＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝

class UpdateView(generic.edit.UpdateView):
    model = Work
    fields = ['name','price','content']
    template_name = 'detail.html'
    success_url = reverse_lazy('timewire:index')


    def form_valid(self, form):
        result = super().form_valid(form)
        messages.info(
            self.request, 'ワークの更新が完了しました')
        return result


update = UpdateView.as_view()

# マイページ要素＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝＝


class GrantView(View):
    def get(self, request,):
        return render(request, 'grant.html')

grant = GrantView.as_view()



class WorkView(View):
    def get(self, request,):
        return render(request, 'work.html')

work = WorkView.as_view()



class FavoriteView(View):
    def get(self, request,):
        return render(request, 'favorite.html')


favorite = FavoriteView.as_view()



class BankView(View):
    def get(self, request,):
        return render(request, 'bank.html')


bank = BankView.as_view()




class ValueView(View):
    def get(self, request,):
        return render(request, 'value.html')


value = ValueView.as_view()




class QuestionView(View):
    def get(self, request,):
        return render(request, 'question.html')


question = QuestionView.as_view()




class SettingView(View):
    def get(self, request,):
        return render(request, 'setting.html')


setting = SettingView.as_view()




class TermView(View):
    def get(self, request,):
        return render(request, 'term.html')


term = TermView.as_view()




class RankingView(View):
    def get(self, request,):
        return render(request, 'ranking.html')


ranking = RankingView.as_view()