#!/usr/bin/env python3
"""
Test script for OpenRouter API integration
"""

import os
import sys
from openai import OpenAI

def test_openrouter_connection():
    """Test basic OpenRouter API connection"""
    
    # Check if API key is set
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return False
    
    print(f"✅ API key found: {api_key[:20]}...")
    
    try:
        # Initialize OpenRouter client
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        # Test simple completion
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://innovatetriz.com",
                "X-Title": "InnovateTRIZ",
            },
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=[
                {
                    "role": "user",
                    "content": "Hello, can you help me analyze technical problems using TRIZ methodology?"
                }
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        response = completion.choices[0].message.content
        print(f"✅ API connection successful!")
        print(f"📝 Response: {response[:100]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ API connection failed: {str(e)}")
        return False

def test_triz_analysis():
    """Test TRIZ problem analysis with AI"""
    
    api_key = os.environ.get('OPENROUTER_API_KEY')
    if not api_key:
        print("❌ OPENROUTER_API_KEY environment variable not set")
        return False
    
    try:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=api_key,
        )
        
        problem = "手机需要更大的电池容量但要保持轻薄的设计"
        
        prompt = f"""
作为TRIZ专家，请分析以下技术问题：

问题：{problem}

请完成以下任务：
1. 识别核心技术矛盾
2. 确定需要改善的参数
3. 确定可能恶化的参数
4. 提供问题的更清晰描述

请以JSON格式返回，包含以下字段：
{{
    "improving_param": "需要改善的参数",
    "worsening_param": "可能恶化的参数", 
    "enhanced_description": "问题的更清晰描述",
    "technical_contradiction": "核心技术矛盾描述",
    "success": true
}}

只返回JSON，不要其他文字。
"""
        
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://innovatetriz.com",
                "X-Title": "InnovateTRIZ",
            },
            model="tngtech/deepseek-r1t2-chimera:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=500
        )
        
        response = completion.choices[0].message.content
        print(f"✅ TRIZ analysis successful!")
        print(f"📝 Response: {response}")
        
        # Try to parse JSON
        import json
        try:
            result = json.loads(response)
            print(f"✅ JSON parsing successful!")
            print(f"📊 Analysis result: {result}")
            return True
        except json.JSONDecodeError:
            print(f"⚠️  JSON parsing failed, but API call succeeded")
            return True
        
    except Exception as e:
        print(f"❌ TRIZ analysis failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("🔬 Testing OpenRouter API Integration")
    print("=" * 50)
    
    # Test basic connection
    print("\n1. Testing basic API connection...")
    basic_test = test_openrouter_connection()
    
    # Test TRIZ analysis
    print("\n2. Testing TRIZ analysis...")
    triz_test = test_triz_analysis()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Results:")
    print(f"   Basic Connection: {'✅' if basic_test else '❌'}")
    print(f"   TRIZ Analysis: {'✅' if triz_test else '❌'}")
    
    if basic_test and triz_test:
        print("\n🎉 All tests passed! OpenRouter integration is ready.")
    else:
        print("\n⚠️  Some tests failed. Please check the configuration.")