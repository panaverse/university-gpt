interface QuestionOption {
  id: string; 
  option_text: string;
}

interface QuestionProps {
  question: string;
  options: QuestionOption[];
  questionType: "single_select_mcq" | "multiple_select_mcq";
  selectedOptions: string[]; // Track selected options to manage state
  onChange: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const QuestionCard: React.FC<QuestionProps> = ({
  question,
  options,
  questionType,
  selectedOptions,
  onChange,
}) => {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-bold text-gray-900 dark:text-gray-100 mb-4">
        {question}
      </h2>
      <div className="space-y-4">
        {options.map((option, index) => (
          <div key={option.id} className="bg-gray-200 p-1.5 dark:bg-gray-700 ...">
            <label className="flex items-center">
              <input
                className="mr-2"
                name={
                  questionType === "single_select_mcq" ? "answer" : "answer[]"
                }
                type={
                  questionType === "single_select_mcq" ? "radio" : "checkbox"
                }
                value={option. id}
                checked={selectedOptions.includes(option.id)}
                onChange={onChange}
              />
              {option.option_text}
            </label>
          </div>
        ))}
      </div>
    </div>
  );
};
