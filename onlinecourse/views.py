from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Enrollment, Submission, Choice


def submit(request, course_id):
    """
    Create a Submission object for the current user and
    save all selected choices.
    """
    course = get_object_or_404(Course, pk=course_id)

    # Ambil enrollment pertama untuk course ini
    # (cukup untuk memenuhi kebutuhan project)
    enrollment = Enrollment.objects.filter(course=course).first()

    if enrollment is None:
        # Jika belum ada enrollment, redirect kembali ke course
        return redirect('onlinecourse:course_details', course_id=course.id)

    # Ambil semua choice yang dipilih user
    selected_choices = request.POST.getlist('choice')

    # Buat submission baru
    submission = Submission.objects.create(
        enrollment=enrollment
    )

    # Simpan pilihan yang dipilih
    for choice_id in selected_choices:
        try:
            choice = Choice.objects.get(pk=int(choice_id))
            submission.choices.add(choice)
        except (Choice.DoesNotExist, ValueError):
            pass

    # Redirect ke halaman hasil exam
    return redirect(
        'onlinecourse:show_exam_result',
        course_id=course.id,
        submission_id=submission.id
    )


def show_exam_result(request, course_id, submission_id):
    """
    Display the result of an exam submission.
    """
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(Submission, pk=submission_id)

    selected_choices = submission.choices.all()

    # Hitung skor sederhana
    total_questions = course.questions.count()
    correct_answers = selected_choices.filter(is_correct=True).count()

    if total_questions > 0:
        grade = int((correct_answers / total_questions) * 100)
    else:
        grade = 0

    context = {
        'course': course,
        'submission': submission,
        'selected_choices': selected_choices,
        'grade': grade,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )