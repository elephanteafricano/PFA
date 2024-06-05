document.addEventListener('DOMContentLoaded', function() {
    const faqs = document.querySelectorAll('.faq-question');

    faqQuestions.forEach(question => {
        const questionText = question.querySelector('p');
        const answers = question.querySelector('.answers');

        questionText.addEventListener('click', () => {
            answers.classList.toggle('visible');
        });

        const buttons = question.querySelectorAll('button');
        buttons.forEach(button => {
            button.addEventListener('click', () => {
                const selectedAnswer = button.textContent.trim();
                checkAnswer(selectedAnswer, question, button); 
            });
        });
    });
    document.querySelectorAll('.faq-question').forEach(question => {
        question.addEventListener('click', () => {
            question.classList.toggle('active');
            
            const container = document.querySelector('.faq-container-left');
            container.style.height = 'auto'; 
            let height = container.scrollHeight + 'px';
            container.style.height = height; 
        });
    });
    
    document.querySelectorAll('.faq-question button').forEach(button => {
        button.addEventListener('click', (event) => {
            event.stopPropagation();
            button.style.backgroundColor = 'white';
        });
    });
    
    let slideIndex = 0;
    showSlides();

    function showSlides() {
        const slides = document.querySelectorAll('.card');
        for (let i = 0; i < slides.length; i++) {
            slides[i].style.display = 'none';
        }
        slideIndex++;
        if (slideIndex > slides.length) { slideIndex = 1 }
        slides[slideIndex - 1].style.display = 'block';
        setTimeout(showSlides, 3000); 
    }
});