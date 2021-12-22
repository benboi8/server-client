def SplitCommand(text):
	return text.split(" ")[0][1:], text[len(text.split(" ")[0]) + 1:]

def Chat(msg):
	command, msg = SplitCommand(msg)
	print(msg)

def Whisper(msg):
	command, msg = SplitCommand(msg)
	print(msg)

def Error(msg):
	print(f"There was an error with the message: {repr(msg)}")

commands = {
	"chat": Chat,
	"whisper": Whisper
}


data = ["/asd Hello", "/chat Hello", "/whisper-[name] Hello"]


for d in data:
	command, msg = SplitCommand(d)
	commands.get(command.lower(), Error)(d)
