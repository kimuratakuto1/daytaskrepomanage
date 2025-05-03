from django.shortcuts import render, redirect, get_object_or_404
from .models import Task, TaskTemplate
from django.utils import timezone
from django.utils.timezone import now
import os
import requests
from django.conf import settings
import openai
from django.http import HttpResponse


#タスク追加
def task_list(request):
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        date = request.POST.get("date")
        task_type = request.POST.get("task_type")
        if title:
            if task_type == "daily":
                TaskTemplate.objects.create(title=title, description=description, is_daily=True)
            else:
                Task.objects.create(title=title, description=description, date=date)
            return redirect('/')
    today = now().date()
    incomplete_tasks = Task.objects.filter(is_done=False,date=today,template__isnull=True)
    completed_today_tasks = Task.objects.filter(is_done=True, completed_at__date=today)
    template_tasks = TaskTemplate.objects.all()
    future_tasks = Task.objects.filter(date__gt=timezone.now().date(), template__isnull=True).order_by('date')
    return render(request, 'task/task_list.html', {
        'incomplete_tasks': incomplete_tasks,
        'completed_today_tasks': completed_today_tasks,
        'today': today,
        'template_tasks': template_tasks,
        'future_tasks': future_tasks,
    })


#タスク編集
def task_edit(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.date = request.POST.get('date')
        task.save()
        return redirect('/')
    
    return render(request, 'task/task_edit.html', {'task': task})

#定型タスク編集
def template_task_edit(request, task_id):
    task = get_object_or_404(TaskTemplate, pk=task_id)
    if request.method == 'POST':
        task.title = request.POST.get('title')
        task.description = request.POST.get('description')
        task.save()
        return redirect('/')
    return render(request, 'template_task/template_task_edit.html', {'task': task})


#タスク消去
def task_delete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')

    return render(request, 'task/task_delete.html', {'task': task})

#定型タスク消去
def template_task_delete(request, task_id):
    task = get_object_or_404(TaskTemplate, pk=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('/')
    return render(request, 'template_task/template_task_delete.html', {'task': task})



#タスク完了
def task_complete(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    if request.method == 'POST':
        task.is_done = True
        task.completed_at = timezone.now()
        task.save()
        return redirect('/')


#業務開始
def start_of_day(request):
    if request.method == 'POST':
        print("POST request received")
        today = timezone.now().date()
        templates = TaskTemplate.objects.filter(is_daily=True)
        
        if not templates:
            print("No daily templates found")
        
        for template in templates:
            print(f"Checking task for: Title: {template.title}, Description: {template.description}, Date: {today}")
            
            # 既存のタスクがあるかどうか確認
            existing_task = Task.objects.filter(
                title=template.title,
                description=template.description,
                date=today
            ).exists()
            
            if not existing_task:
                print(f"Creating task: Title: {template.title}, Description: {template.description}, Date: {today}")
                Task.objects.create(
                    title=template.title,
                    description=template.description,
                    date=today
                )
            else:
                print(f"Task already exists for: {template.title}, {template.description}")
        
        print("Task creation process completed.")
        return redirect('/')  # トップページにリダイレクト



# 業務終了
def end_of_day(request):
    if request.method == 'POST':
        today = timezone.now().date()
        formatted_today = today.strftime("%Y年%m月%d日")
        completed_tasks = Task.objects.filter(is_done=True, completed_at__date=today)
        if not completed_tasks.exists():
            return render(request, 'report/end_of_day_report.html', {'report': '本日は完了したタスクがありません。'})
        task_summaries = [
            f"- {task.title}： {task.description or '説明なし'}"
            for task in completed_tasks
        ]
        prompt = ("今日行った業務について、以下のタスクをもとに日本語で業務日報を作成してください。内容は簡潔で、業務の進捗や成果を強調し、最終的な成果や次のステップを示唆してください。\n\n"
        + "\n".join(task_summaries)
        + "日報は業務を振り返る形で記述してください。例えば、タスクの進捗状況や課題、今後の対応予定について記載してください。"
        )

        try:
            client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
            )
            report = response.choices[0].message.content
        except Exception as e:
            print(f"Error generating report: {e}")
            report = "日報作成中に問題が発生しました"
        return render(request, 'report/end_of_day_report.html', {'report': report, 'today': formatted_today})