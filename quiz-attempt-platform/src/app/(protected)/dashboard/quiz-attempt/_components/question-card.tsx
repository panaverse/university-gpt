interface QuestionOption {
    value: string;
    label: string;
  }
  
interface QuestionProps {
    question: string;
    options: QuestionOption[];
    questionType: 'single_select_mcq' | 'multiple_select_mcq';
    onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
  }

export const QuestionCard: React.FC<QuestionProps> = ({ question, options, questionType, onChange }) => (
    <div className="mb-6">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-2">{question}</h2>
      <div className="space-y-4">
        {options.map((option, index) => (
          <div key={index} className="bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-900 dark:text-gray-100 rounded-md p-4 transition-colors">
            <label className="flex items-center">
              <input className="mr-2"
                     name={questionType === 'single_select_mcq' ? 'answer' : 'answer[]'}
                     type={questionType === 'single_select_mcq' ? 'radio' : 'checkbox'}
                     value={option.value}
                     onChange={onChange} />
              {option.label}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
