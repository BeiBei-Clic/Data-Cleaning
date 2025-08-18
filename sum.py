def generate_summary(self, text: str, filename: str) -> str:
    """生成摘要（采用分块清洗相同的分块逻辑）"""
    CHUNK_SIZE = 2000 # 文件大小超过2000字符时进行分块
    OVERLAP_SIZE = self.overlap_size

    prompt_template = """请从以下文本中提取关键信息作为部分摘要：

当前文档: {filename}
分块: {chunk_num}/{total_chunks}

要求：
1. 提取本部分的核心内容
2. 保持客观事实
3. 用简洁的短语列出要点

文本内容：
{chunk_text}"""

    final_prompt = """请将以下部分摘要合并为完整摘要，按结构整理：

【标题】<保持原文标题不变>

- 项目背景（整合各部分背景）
- 主要措施（合并所有措施，去重后保留3-5点）
- 取得成效（合并量化成果）
- 经验教训（整合关键经验）

要求：最终摘要不超过600字

部分摘要：
{partial_summaries}"""

    # 分块逻辑（与clean_text_chunks保持一致）
    def split_into_chunks(text: str) -> list:
        if len(text) <= CHUNK_SIZE:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + CHUNK_SIZE
            if end < len(text):
                # 优先在段落边界分割
                for separator in ['\n\n', '。', '\n', ' ']:
                    search_start = max(start + CHUNK_SIZE - OVERLAP_SIZE, start)
                    split_pos = text.rfind(separator, search_start, end)
                    if split_pos != -1:
                        end = split_pos + len(separator)
                        break
            chunks.append(text[start:end].strip())
            start = max(end - OVERLAP_SIZE, start + 1)
        return chunks

    # 处理单个分块
    def process_chunk(chunk: str, chunk_num: int, total_chunks: int) -> str:
        prompt = prompt_template.format(
            filename=filename,
            chunk_num=chunk_num + 1,
            total_chunks=total_chunks,
            chunk_text=chunk
        )

        for attempt in range(self.max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.3,
                    max_tokens=300  # 限制部分摘要长度
                )
                if response and response.choices:
                    return response.choices[0].message.content
            except Exception as e:
                print(f"分块{chunk_num + 1}第{attempt + 1}次尝试失败: {str(e)}")
                if attempt < self.max_retries - 1:
                    time.sleep(30)
        return f"[分块{chunk_num + 1}摘要生成失败]"

    # 主流程
    chunks = split_into_chunks(text)
    if len(chunks) == 1:
        # 小文件直接处理（使用原始提示模板）
        prompt = f"""请从以下案例中提取关键信息，按以下结构总结：

【标题】<保持原文标题不变>

- 项目背景
- 主要措施（3-5点）
- 取得成效（2-3项具体成果）
- 经验教训（3-5点）

要求：字数不超过600字

案例[{filename}]：
{text}"""
        return self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3
        ).choices[0].message.content

    # 大文件分块处理
    print(f"📑 大文件分块处理: {filename} (共{len(chunks)}块)")

    partial_summaries = []
    for i, chunk in enumerate(chunks):
        print(f"  正在处理分块 {i + 1}/{len(chunks)}...")
        chunk_summary = process_chunk(chunk, i, len(chunks))
        partial_summaries.append(f"=== 分块 {i + 1} ===\n{chunk_summary}")

    # 合并摘要
    print("🔄 合并部分摘要...")
    combined_text = "\n\n".join(partial_summaries)
    final_summary = self.client.chat.completions.create(
        model=self.model,
        messages=[{"role": "user", "content": final_prompt.format(partial_summaries=combined_text)}],
        temperature=0.3,
        max_tokens=600
    ).choices[0].message.content

    return final_summary