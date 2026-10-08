import os
import signal

from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs.conversational_ai.conversation import Conversation
from elevenlabs.conversational_ai.default_audio_interface import DefaultAudioInterface


def main():
    load_dotenv()

    agent_id = os.getenv("AGENT_ID")
    api_key = os.getenv("ELEVENLABS_API_KEY")

    if not agent_id:
        raise RuntimeError("Set AGENT_ID in your .env file.")

    client = ElevenLabs(api_key=api_key)

    conversation = Conversation(
        client,
        agent_id,
        requires_auth=bool(api_key),
        audio_interface=DefaultAudioInterface(),
        callback_agent_response=lambda response: print(f"Agent: {response}"),
        callback_user_transcript=lambda transcript: print(f"You: {transcript}"),
    )

    signal.signal(signal.SIGINT, lambda *_: conversation.end_session())

    conversation.start_session()
    conversation_id = conversation.wait_for_session_end()

    print(f"\nConversation ID: {conversation_id}")


if __name__ == "__main__":
    main()
