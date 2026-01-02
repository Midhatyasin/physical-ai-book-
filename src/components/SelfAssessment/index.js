import React, {useState} from 'react';
import clsx from 'clsx';
import styles from './styles.module.css';

export default function SelfAssessment({
  title = 'Self-Assessment',
  questions = [],
  showResults = true,
}) {
  const [answers, setAnswers] = useState({});
  const [submitted, setSubmitted] = useState(false);
  const [score, setScore] = useState(0);

  const handleAnswer = (questionId, optionIndex) => {
    if (submitted) return;
    setAnswers(prev => ({
      ...prev,
      [questionId]: optionIndex,
    }));
  };

  const handleSubmit = () => {
    let correctCount = 0;
    questions.forEach(q => {
      if (answers[q.id] === q.correctAnswer) {
        correctCount++;
      }
    });
    setScore(Math.round((correctCount / questions.length) * 100));
    setSubmitted(true);
  };

  const handleReset = () => {
    setAnswers({});
    setSubmitted(false);
    setScore(0);
  };

  return (
    <div className={styles.container}>
      <h3 className={styles.title}>{title}</h3>

      <div className={styles.questions}>
        {questions.map((question, qIndex) => (
          <div key={question.id} className={styles.question}>
            <p className={styles.questionText}>
              <span className={styles.questionNumber}>{qIndex + 1}.</span>
              {question.text}
            </p>

            <div className={styles.options}>
              {question.options.map((option, oIndex) => {
                const isSelected = answers[question.id] === oIndex;
                const isCorrect = submitted && oIndex === question.correctAnswer;
                const isWrong = submitted && isSelected && oIndex !== question.correctAnswer;

                return (
                  <button
                    key={oIndex}
                    className={clsx(styles.option, {
                      [styles.selected]: isSelected,
                      [styles.correct]: isCorrect,
                      [styles.wrong]: isWrong,
                      [styles.disabled]: submitted,
                    })}
                    onClick={() => handleAnswer(question.id, oIndex)}
                    disabled={submitted}
                  >
                    <span className={styles.optionLetter}>
                      {String.fromCharCode(65 + oIndex)}
                    </span>
                    <span className={styles.optionText}>{option}</span>
                    {submitted && isCorrect && <span className={styles.feedbackIcon}>✓</span>}
                    {submitted && isWrong && <span className={styles.feedbackIcon}>✗</span>}
                  </button>
                );
              })}
            </div>

            {submitted && question.explanation && (
              <div className={styles.explanation}>
                <strong>Explanation:</strong> {question.explanation}
              </div>
            )}
          </div>
        ))}
      </div>

      {!submitted ? (
        <button
          className={styles.submitBtn}
          onClick={handleSubmit}
          disabled={Object.keys(answers).length < questions.length}
        >
          Check Answers
        </button>
      ) : (
        <div className={styles.results}>
          <div className={clsx(styles.score, {
            [styles.excellent]: score >= 90,
            [styles.good]: score >= 70 && score < 90,
            [styles.needsWork]: score < 70,
          })}>
            Score: {score}%
          </div>
          <p className={styles.resultMessage}>
            {score >= 90 ? 'Excellent! You have a strong understanding of the material.' :
             score >= 70 ? 'Good job! Review the missed questions to strengthen your knowledge.' :
             'Keep learning! Review the chapter content and try again.'}
          </p>
          <button className={styles.resetBtn} onClick={handleReset}>
            Try Again
          </button>
        </div>
      )}
    </div>
  );
}
