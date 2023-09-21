document.addEventListener('DOMContentLoaded', function() {
  const questionContainer = document.getElementById('question-container');
  const optionsContainer = document.getElementById('options');
  const prevButton = document.getElementById('prev-btn');
  const nextButton = document.getElementById('next-btn');
  const submitButton = document.getElementById('submit-btn');
  const resultsDiv = document.getElementById('results');
  const scoreValueSpan = document.getElementById('score-value');

  const questions = [
    {
      question: 'What is the capital of France?',
      options: ['Paris', 'London', 'Berlin'],
      correctAnswer: 'Paris'
    },
    {
      question: 'Which planet is known as the "Red Planet"?',
      options: ['Earth', 'Mars', 'Venus'],
      correctAnswer: 'Mars'
    },
    {
      question: 'Who wrote the play "Romeo and Juliet"?',
      options: ['William Shakespeare', 'Charles Dickens', 'Jane Austen'],
      correctAnswer: 'William Shakespeare'
    },
    {
      question: 'What is the world\'s largest ocean?',
      options: ['Atlantic Ocean', 'Indian Ocean', 'Pacific Ocean'],
      correctAnswer: 'Pacific Ocean'
    },
    {
      question: 'What is the capital of Japan?',
      options: ['Tokyo', 'Beijing', 'Seoul'],
      correctAnswer: 'Tokyo'
    },
    // Add more questions here
  ];

  let currentQuestionIndex = 0;

  function showQuestion(index) {
    const questionObj = questions[index];
    questionContainer.querySelector('h3').textContent = questionObj.question;

    optionsContainer.innerHTML = '';

    questionObj.options.forEach((option, optionIndex) => {
      const label = document.createElement('label');
      const input = document.createElement('input');
      input.type = 'radio';
      input.name = 'answer';
      input.value = optionIndex === questionObj.options.indexOf(questionObj.correctAnswer) ? 'correct' : 'incorrect';
      label.appendChild(input);
      label.appendChild(document.createTextNode(option));
      optionsContainer.appendChild(label);
    });

    prevButton.disabled = index === 0;
    nextButton.disabled = index === questions.length - 1;
    submitButton.classList.toggle('hidden', index !== questions.length - 1);
  }

  prevButton.addEventListener('click', function() {
    currentQuestionIndex--;
    showQuestion(currentQuestionIndex);
  });

  nextButton.addEventListener('click', function() {
    currentQuestionIndex++;
    showQuestion(currentQuestionIndex);
  });

  const quizForm = document.getElementById('quiz-form');
  quizForm.addEventListener('submit', function(event) {
    event.preventDefault(); // Prevent form submission

    let score = 0;

    const selectedAnswers = quizForm.querySelectorAll('input[name="answer"]:checked');
    selectedAnswers.forEach(selectedAnswer => {
      if (selectedAnswer.value === 'correct') {
        score++;
      }
    });

    scoreValueSpan.textContent = score;
    resultsDiv.classList.remove('hidden');
  });

  // Show the first question when the page loads
  showQuestion(currentQuestionIndex);
});
