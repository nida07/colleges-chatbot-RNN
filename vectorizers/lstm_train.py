import pandas as pd
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Embedding, LSTM, Dense
import pickle


data = pd.read_csv(r'C:\Users\admin\Downloads\Chatbot_completed (3)\Chatbot_completed\Chatbot_completed\Chatbot\vectorizers\models\topical_chat.csv')

# extracting the features and labels from the dataset. values converts the column data into a NumPy array.  
#X will contain an array of text messages or textual data, which will serve as the input features for our model.
#y will contain an array of sentiment labels corresponding to each text message in X, which will serve as the
# target variable for our model 

X = data['message'].values
y = data['sentiment'].values

#creates a boolean array by checking 
#if each element in the array y is equal to the string 'Happy'

y = (y == 'Happy').astype(int)

#X_train and y_train will contain the features and labels for 
#the training set, while X_test and y_test will contain the features and labels for the testing set.
#random_state =  the data will be split in the same way every time the code is run.


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

#Tokenizer class is used to convert text data into sequences of tokens or integers
#The fit_on_texts() method is called to update the 
#tokenizer's vocabulary based on the text data

tokenizer = Tokenizer()
tokenizer.fit_on_texts(X_train)
#converting the text data in X_train and X_test into sequences of integers.
X_train_seq = tokenizer.texts_to_sequences(X_train)
X_test_seq = tokenizer.texts_to_sequences(X_test)

#allows for the efficient handling of variable-length input data by machine learning models
# max number of sequences in each length and find the maximum and it set as pad_sequences
max_len = max(len(seq) for seq in X_train_seq)
X_train_padded = pad_sequences(X_train_seq, maxlen=max_len, padding='post')
X_test_padded = pad_sequences(X_test_seq, maxlen=max_len, padding='post')

# Build RNN Model
vocab_size = len(tokenizer.word_index) + 1

# layers 3
# Embedding(input dim, output dimension, input_length, initialization method)  uniform distribution
# lstm uses 100 memory cell
# dense (tot no of tags , activation function)


# Define model architecture
#sequential,is a model constructor

model = Sequential()
model.add(Embedding(input_dim=vocab_size, output_dim=100, input_length=max_len, embeddings_initializer='uniform'))
model.add(LSTM(100))
model.add(Dense(1, activation='sigmoid'))

model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the Model

#validation_data=Iterate over the training dataset (X_train_padded, y_train) for the specified number of epochs.
#epoch change 10,20,40,...etc

model.fit(X_train_padded, y_train, epochs=10, validation_data=(X_test_padded, y_test))

# Save the Model and Tokenizer to Files
model.save('sentiment_model.h5')

# Save the tokenizer to a pickle file 
#serialization
#  protocol=pickle.HIGHEST_PROTOCOL=>>ensures compatibility with different versions of Python 


with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)
