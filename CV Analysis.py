import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
import json
import os
import re
from datetime import datetime
from collections import Counter
import math

class PersonalityAnalyzer:
    def __init__(self):
        # Big Five personality traits
        self.traits = {
            'Openness': 0,
            'Conscientiousness': 0, 
            'Extraversion': 0,
            'Agreeableness': 0,
            'Emotional Stability': 0
        }
        
        # Keyword dictionaries for personality prediction
        self.personality_keywords = {
            'Openness': {
                'high': ['creative', 'innovative', 'artistic', 'imaginative', 'curious', 'original', 
                        'inventive', 'versatile', 'adaptable', 'experimental', 'design', 'research',
                        'development', 'exploration', 'brainstorming', 'conceptual', 'theoretical',
                        'abstract', 'philosophical', 'unconventional', 'novel', 'cutting-edge'],
                'low': ['traditional', 'conventional', 'routine', 'standard', 'established',
                       'systematic', 'structured', 'methodical', 'practical', 'conservative']
            },
            'Conscientiousness': {
                'high': ['organized', 'detailed', 'responsible', 'reliable', 'thorough', 'systematic',
                        'methodical', 'disciplined', 'efficient', 'punctual', 'planning', 'scheduled',
                        'achievement', 'goal-oriented', 'dedicated', 'committed', 'focused', 'precise',
                        'quality', 'standards', 'deadline', 'completion', 'accomplishment'],
                'low': ['flexible', 'spontaneous', 'casual', 'relaxed', 'informal', 'adaptable']
            },
            'Extraversion': {
                'high': ['leadership', 'team', 'collaboration', 'communication', 'presentation',
                        'networking', 'social', 'outgoing', 'energetic', 'enthusiastic', 'dynamic',
                        'engaging', 'interactive', 'public speaking', 'relationship building',
                        'influencing', 'motivating', 'coordinating', 'facilitating', 'mentoring'],
                'low': ['independent', 'individual', 'solitary', 'analytical', 'research',
                       'documentation', 'writing', 'technical', 'focused', 'concentrated']
            },
            'Agreeableness': {
                'high': ['cooperative', 'collaborative', 'supportive', 'helpful', 'team player',
                        'consensus', 'harmony', 'diplomatic', 'understanding', 'empathetic',
                        'service', 'assistance', 'volunteer', 'community', 'charity', 'caring',
                        'nurturing', 'patient', 'kind', 'considerate', 'respectful'],
                'low': ['competitive', 'challenging', 'assertive', 'direct', 'critical',
                       'analytical', 'objective', 'independent', 'decisive']
            },
            'Emotional Stability': {
                'high': ['calm', 'stable', 'consistent', 'resilient', 'composed', 'confident',
                        'steady', 'balanced', 'reliable', 'stress management', 'pressure',
                        'challenging', 'difficult', 'crisis', 'problem-solving', 'adaptable',
                        'flexible', 'managing', 'handling', 'coping'],
                'low': ['sensitive', 'reactive', 'emotional', 'stressed', 'anxious', 'worried']
            }
        }
        
        # Experience level indicators
        self.experience_indicators = {
            'senior': ['senior', 'lead', 'principal', 'director', 'manager', 'head', 'chief', 'vp', 'vice president'],
            'mid': ['specialist', 'analyst', 'consultant', 'coordinator', 'supervisor'],
            'junior': ['junior', 'entry', 'assistant', 'associate', 'intern', 'trainee']
        }
        
        # Industry categories
        self.industries = {
            'tech': ['software', 'technology', 'IT', 'computer', 'programming', 'development', 'data'],
            'business': ['business', 'management', 'marketing', 'sales', 'finance', 'accounting'],
            'creative': ['design', 'creative', 'art', 'media', 'advertising', 'content'],
            'research': ['research', 'science', 'analysis', 'academic', 'laboratory']
        }
        
    def extract_text_features(self, text):
        """Extract various features from resume text"""
        text_lower = text.lower()
        words = re.findall(r'\b\w+\b', text_lower)
        
        features = {
            'total_words': len(words),
            'unique_words': len(set(words)),
            'avg_word_length': sum(len(word) for word in words) / len(words) if words else 0,
            'sentence_count': len(re.findall(r'[.!?]+', text)),
            'exclamation_count': text.count('!'),
            'question_count': text.count('?'),
            'capital_words': len(re.findall(r'\b[A-Z]{2,}\b', text)),
            'numbers_count': len(re.findall(r'\b\d+\b', text)),
        }
        
        # Education indicators
        education_keywords = ['university', 'college', 'degree', 'bachelor', 'master', 'phd', 'doctorate']
        features['education_mentions'] = sum(text_lower.count(word) for word in education_keywords)
        
        # Achievement indicators  
        achievement_keywords = ['achieved', 'accomplished', 'awarded', 'recognized', 'improved', 'increased']
        features['achievement_mentions'] = sum(text_lower.count(word) for word in achievement_keywords)
        
        # Leadership indicators
        leadership_keywords = ['led', 'managed', 'directed', 'supervised', 'coordinated', 'headed']
        features['leadership_mentions'] = sum(text_lower.count(word) for word in leadership_keywords)
        
        return features
    
    def calculate_personality_scores(self, text, features):
        """Calculate personality trait scores based on text analysis"""
        text_lower = text.lower()
        scores = {}
        
        for trait, keywords in self.personality_keywords.items():
            high_score = sum(text_lower.count(word) for word in keywords['high'])
            low_score = sum(text_lower.count(word) for word in keywords['low'])
            
            # Base score calculation
            base_score = (high_score - low_score) + 50  # Normalize around 50
            
            # Adjust based on text features
            if trait == 'Conscientiousness':
                # More organized language structure indicates higher conscientiousness
                if features['avg_word_length'] > 5:
                    base_score += 5
                if features['achievement_mentions'] > 2:
                    base_score += 10
                    
            elif trait == 'Extraversion':
                # More social and leadership language
                if features['leadership_mentions'] > 1:
                    base_score += 10
                if features['exclamation_count'] > 0:
                    base_score += 5
                    
            elif trait == 'Openness':
                # Diverse vocabulary and creative language
                vocab_diversity = features['unique_words'] / features['total_words'] if features['total_words'] > 0 else 0
                if vocab_diversity > 0.6:
                    base_score += 10
                    
            elif trait == 'Agreeableness':
                # Collaborative and service-oriented language
                collab_words = ['team', 'collaborate', 'help', 'support', 'assist']
                collab_score = sum(text_lower.count(word) for word in collab_words)
                base_score += collab_score * 2
                
            elif trait == 'Emotional Stability':
                # Consistent, calm language patterns
                if features['sentence_count'] > 10 and features['exclamation_count'] == 0:
                    base_score += 5
            
            # Normalize score to 0-100 range
            scores[trait] = max(0, min(100, base_score))
            
        return scores
    
    def determine_experience_level(self, text):
        """Determine experience level from resume text"""
        text_lower = text.lower()
        
        senior_count = sum(text_lower.count(word) for word in self.experience_indicators['senior'])
        mid_count = sum(text_lower.count(word) for word in self.experience_indicators['mid'])
        junior_count = sum(text_lower.count(word) for word in self.experience_indicators['junior'])
        
        if senior_count > mid_count and senior_count > junior_count:
            return "Senior Level"
        elif mid_count > junior_count:
            return "Mid Level"
        else:
            return "Entry Level"
    
    def identify_industry(self, text):
        """Identify likely industry based on keywords"""
        text_lower = text.lower()
        industry_scores = {}
        
        for industry, keywords in self.industries.items():
            score = sum(text_lower.count(word) for word in keywords)
            industry_scores[industry] = score
        
        if max(industry_scores.values()) > 0:
            return max(industry_scores, key=industry_scores.get).title()
        return "General"
    
    def generate_personality_report(self, scores, experience_level, industry, features):
        """Generate a comprehensive personality report"""
        report = []
        report.append("=== PERSONALITY ANALYSIS REPORT ===\n")
        
        # Big Five Scores
        report.append("BIG FIVE PERSONALITY TRAITS:\n")
        for trait, score in scores.items():
            level = "High" if score > 70 else "Moderate" if score > 40 else "Low"
            report.append(f"• {trait}: {score:.1f}/100 ({level})")
        
        report.append(f"\nEXPERIENCE LEVEL: {experience_level}")
        report.append(f"LIKELY INDUSTRY: {industry}")
        
        # Detailed trait interpretations
        report.append("\n=== DETAILED TRAIT ANALYSIS ===\n")
        
        # Openness
        openness = scores['Openness']
        if openness > 70:
            report.append("OPENNESS (High): This candidate likely enjoys new experiences, is creative and imaginative. They may thrive in roles requiring innovation and adaptability.")
        elif openness > 40:
            report.append("OPENNESS (Moderate): This candidate shows balanced openness to new experiences while maintaining practical focus.")
        else:
            report.append("OPENNESS (Low): This candidate likely prefers routine and established methods. They may excel in structured, detail-oriented roles.")
        
        # Conscientiousness  
        conscientiousness = scores['Conscientiousness']
        if conscientiousness > 70:
            report.append("CONSCIENTIOUSNESS (High): Highly organized and reliable. Likely to meet deadlines and maintain high quality standards.")
        elif conscientiousness > 40:
            report.append("CONSCIENTIOUSNESS (Moderate): Shows good organizational skills with balanced flexibility.")
        else:
            report.append("CONSCIENTIOUSNESS (Low): May prefer flexible work environments and spontaneous approaches.")
        
        # Extraversion
        extraversion = scores['Extraversion']
        if extraversion > 70:
            report.append("EXTRAVERSION (High): Likely energetic and outgoing. May excel in leadership, sales, or client-facing roles.")
        elif extraversion > 40:
            report.append("EXTRAVERSION (Moderate): Comfortable in both individual and team settings.")
        else:
            report.append("EXTRAVERSION (Low): Likely prefers independent work and smaller team environments.")
        
        # Agreeableness
        agreeableness = scores['Agreeableness']
        if agreeableness > 70:
            report.append("AGREEABLENESS (High): Cooperative and team-oriented. Likely to work well in collaborative environments.")
        elif agreeableness > 40:
            report.append("AGREEABLENESS (Moderate): Balanced approach to cooperation and assertiveness.")
        else:
            report.append("AGREEABLENESS (Low): May be more competitive and direct in approach. Could excel in challenging, results-driven roles.")
        
        # Emotional Stability
        stability = scores['Emotional Stability']
        if stability > 70:
            report.append("EMOTIONAL STABILITY (High): Likely handles stress well and remains calm under pressure.")
        elif stability > 40:
            report.append("EMOTIONAL STABILITY (Moderate): Generally stable with normal stress responses.")
        else:
            report.append("EMOTIONAL STABILITY (Low): May be more sensitive to stress. Could benefit from supportive work environments.")
        
        # Role recommendations
        report.append(f"\n=== ROLE RECOMMENDATIONS ===\n")
        
        if scores['Extraversion'] > 60 and scores['Agreeableness'] > 60:
            report.append("• Team Leadership roles")
            report.append("• Customer Relations")
            report.append("• Sales and Marketing")
        
        if scores['Conscientiousness'] > 70 and scores['Openness'] < 50:
            report.append("• Project Management")
            report.append("• Quality Assurance")
            report.append("• Operations")
        
        if scores['Openness'] > 70 and scores['Conscientiousness'] > 60:
            report.append("• Research and Development")
            report.append("• Creative roles")
            report.append("• Innovation Management")
        
        if scores['Emotional Stability'] > 70 and scores['Conscientiousness'] > 60:
            report.append("• Crisis Management")
            report.append("• High-pressure environments")
            report.append("• Strategic roles")
        
        return "\n".join(report)

class PersonalityAnalyzerGUI:
    def __init__(self):
        self.analyzer = PersonalityAnalyzer()
        self.root = tk.Tk()
        self.root.title("Resume Personality Analyzer")
        self.root.geometry("1000x700")
        
        self.analysis_history = []
        
        self.setup_gui()
    
    def setup_gui(self):
        """Setup the GUI components"""
        # Main notebook for tabs
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Analysis Tab
        analysis_frame = ttk.Frame(notebook)
        notebook.add(analysis_frame, text="Resume Analysis")
        
        # Input section
        input_frame = ttk.LabelFrame(analysis_frame, text="Resume Input")
        input_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # File upload button
        file_frame = ttk.Frame(input_frame)
        file_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(file_frame, text="Upload Resume File", 
                  command=self.upload_file).pack(side=tk.LEFT, padx=5)
        ttk.Button(file_frame, text="Clear Text", 
                  command=self.clear_text).pack(side=tk.LEFT, padx=5)
        
        # Text input area
        ttk.Label(input_frame, text="Or paste resume text below:").pack(anchor=tk.W, padx=10, pady=(10,0))
        self.text_input = scrolledtext.ScrolledText(input_frame, height=15, width=80)
        self.text_input.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Analysis button
        ttk.Button(input_frame, text="Analyze Personality", 
                  command=self.analyze_resume).pack(pady=10)
        
        # Results Tab
        results_frame = ttk.Frame(notebook)
        notebook.add(results_frame, text="Analysis Results")
        
        # Results display
        self.results_text = scrolledtext.ScrolledText(results_frame, height=30, width=100)
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # History Tab
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Analysis History")
        
        # History controls
        history_controls = ttk.Frame(history_frame)
        history_controls.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(history_controls, text="Export History", 
                  command=self.export_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(history_controls, text="Clear History", 
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        
        # History list
        self.history_tree = ttk.Treeview(history_frame, 
                                        columns=('Timestamp', 'Experience', 'Industry', 'Top_Trait'),
                                        show='headings', height=15)
        
        self.history_tree.heading('Timestamp', text='Analysis Time')
        self.history_tree.heading('Experience', text='Experience Level')
        self.history_tree.heading('Industry', text='Industry')
        self.history_tree.heading('Top_Trait', text='Dominant Trait')
        
        self.history_tree.column('Timestamp', width=150)
        self.history_tree.column('Experience', width=120)
        self.history_tree.column('Industry', width=100)
        self.history_tree.column('Top_Trait', width=150)
        
        history_scroll = ttk.Scrollbar(history_frame, orient=tk.VERTICAL, command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=history_scroll.set)
        
        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=5)
        history_scroll.pack(side=tk.RIGHT, fill=tk.Y, pady=5)
        
        # Status bar
        self.status_label = ttk.Label(self.root, text="Ready for analysis", relief=tk.SUNKEN)
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)
    
    def upload_file(self):
        """Upload and read resume file"""
        file_types = [
            ("Text files", "*.txt"),
            ("All files", "*.*")
        ]
        
        filename = filedialog.askopenfilename(
            title="Select Resume File",
            filetypes=file_types
        )
        
        if filename:
            try:
                with open(filename, 'r', encoding='utf-8') as file:
                    content = file.read()
                    self.text_input.delete(1.0, tk.END)
                    self.text_input.insert(1.0, content)
                    self.status_label.config(text=f"Loaded file: {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to read file: {str(e)}")
    
    def clear_text(self):
        """Clear the text input area"""
        self.text_input.delete(1.0, tk.END)
        self.status_label.config(text="Text cleared")
    
    def analyze_resume(self):
        """Analyze the resume text for personality traits"""
        text = self.text_input.get(1.0, tk.END).strip()
        
        if not text:
            messagebox.showerror("Error", "Please enter or upload resume text")
            return
        
        if len(text) < 100:
            messagebox.showwarning("Warning", "Resume text seems too short for accurate analysis")
        
        try:
            # Perform analysis
            self.status_label.config(text="Analyzing resume...")
            
            # Extract features
            features = self.analyzer.extract_text_features(text)
            
            # Calculate personality scores
            personality_scores = self.analyzer.calculate_personality_scores(text, features)
            
            # Determine additional attributes
            experience_level = self.analyzer.determine_experience_level(text)
            industry = self.analyzer.identify_industry(text)
            
            # Generate report
            report = self.analyzer.generate_personality_report(
                personality_scores, experience_level, industry, features
            )
            
            # Display results
            self.results_text.delete(1.0, tk.END)
            self.results_text.insert(1.0, report)
            
            # Add to history
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            dominant_trait = max(personality_scores, key=personality_scores.get)
            
            history_entry = {
                'timestamp': timestamp,
                'experience_level': experience_level,
                'industry': industry,
                'dominant_trait': f"{dominant_trait} ({personality_scores[dominant_trait]:.1f})",
                'personality_scores': personality_scores,
                'full_report': report
            }
            
            self.analysis_history.append(history_entry)
            self.update_history_display()
            
            self.status_label.config(text="Analysis completed successfully")
            
            # Switch to results tab
            notebook = self.root.children['!notebook']
            notebook.select(1)  # Select results tab
            
        except Exception as e:
            messagebox.showerror("Error", f"Analysis failed: {str(e)}")
            self.status_label.config(text="Analysis failed")
    
    def update_history_display(self):
        """Update the history tree display"""
        # Clear existing items
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        # Add history entries
        for entry in reversed(self.analysis_history):  # Show newest first
            self.history_tree.insert('', 'end', values=(
                entry['timestamp'],
                entry['experience_level'],
                entry['industry'],
                entry['dominant_trait']
            ))
    
    def export_history(self):
        """Export analysis history to file"""
        if not self.analysis_history:
            messagebox.showwarning("Warning", "No analysis history to export")
            return
        
        filename = filedialog.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            title="Save Analysis History"
        )
        
        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(self.analysis_history, f, indent=2, ensure_ascii=False)
                messagebox.showinfo("Success", f"History exported to {filename}")
                self.status_label.config(text=f"History exported to {os.path.basename(filename)}")
            except Exception as e:
                messagebox.showerror("Error", f"Export failed: {str(e)}")
    
    def clear_history(self):
        """Clear analysis history"""
        if messagebox.askyesno("Confirmation", "Are you sure you want to clear all analysis history?"):
            self.analysis_history = []
            self.update_history_display()
            self.status_label.config(text="History cleared")
    
    def run(self):
        """Run the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = PersonalityAnalyzerGUI()
    app.run()
