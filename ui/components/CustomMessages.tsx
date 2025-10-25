"use client";

import { MessagesProps } from "@copilotkit/react-ui/dist/components/chat/props";
import { AgentActivityIndicator } from "./AgentActivityIndicator";

export function CustomMessages(props: MessagesProps) {
  const {
    inProgress,
    children,
    RenderMessage,
    AssistantMessage,
    UserMessage,
    ErrorMessage,
    ImageRenderer,
    onRegenerate,
    onCopy,
    onThumbsUp,
    onThumbsDown,
    markdownTagRenderers,
    chatError,
    messages,
  } = props;

  return (
    <>
      {/* Render all messages */}
      {messages?.map((message, index) => {
        const isCurrentMessage = index === (messages?.length || 0) - 1;
        return RenderMessage ? (
          <RenderMessage
            key={index}
            message={message}
            inProgress={inProgress}
            index={index}
            isCurrentMessage={isCurrentMessage}
            AssistantMessage={AssistantMessage}
            UserMessage={UserMessage}
            ImageRenderer={ImageRenderer}
            onRegenerate={onRegenerate}
            onCopy={onCopy}
            onThumbsUp={onThumbsUp}
            onThumbsDown={onThumbsDown}
            markdownTagRenderers={markdownTagRenderers}
          />
        ) : null;
      })}
      
      {/* Activity Indicator */}
      <AgentActivityIndicator />
      
      {/* Error Message */}
      {chatError && ErrorMessage && <ErrorMessage error={chatError} isCurrentMessage />}
      
      {/* Children (suggestions, etc.) */}
      {children}
    </>
  );
}

