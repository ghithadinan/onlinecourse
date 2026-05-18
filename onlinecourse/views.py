from django.shortcuts import get_object_or_404, redirect, render
from .models import Course, Enrollment, Submission, Choice


def submit(request, course_id):
    """
    Create a Submission object for the current user and
    save all selected choices.
    """
    course = get_object_or_404(Course, pk=course_id)

    # Ambil enrollment pertama untuk course ini
    enrollment = Enrollment.objects.filter(course=course).first()

    if enrollment is None:
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

    # ID pilihan yang dipilih user
    selected_ids = submission.choices.values_list('id', flat=True)

    # Hitung total nilai yang diperoleh dan total nilai maksimal
    total_score = 0
    possible_score = 0

    for question in course.questions.all():
        possible_score += question.grade

        # Semua choice yang benar untuk question ini
        correct_ids = set(
            question.choices.filter(is_correct=True)
            .values_list('id', flat=True)
        )

        # Semua choice yang dipilih user untuk question ini
        selected_for_question = set(
            submission.choices.filter(question=question)
            .values_list('id', flat=True)
        )

        # Nilai hanya diberikan jika pilihan user persis sama
        # dengan jawaban yang benar
        if correct_ids == selected_for_question:
            total_score += question.grade

    context = {
        'course': course,
        'selected_ids': selected_ids,
        'grade': total_score,
        'possible': possible_score,
    }

    return render(
        request,
        'onlinecourse/exam_result_bootstrap.html',
        context
    )