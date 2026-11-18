import { useState, useRef, useCallback } from 'react';
import { FolderOpen, LayoutTemplate, Music, Type, CheckCircle2, Film } from 'lucide-react';
import './Sidebar.css';

import { type MediaFile } from '../types';

interface SidebarProps {
  onVideoUpload: (file: MediaFile) => void;
  onAudioUpload?: (file: MediaFile) => void;
  onReferenceUpload?: (file: MediaFile) => void;
}

const formatBytes = (bytes: number): string => {
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
};

const Sidebar = ({ onVideoUpload, onAudioUpload, onReferenceUpload }: SidebarProps) => {
  const [activeTab, setActiveTab] = useState('media');
  const [mediaFiles, setMediaFiles] = useState<MediaFile[]>([]);
  const [audioFiles, setAudioFiles] = useState<MediaFile[]>([]);
  const [referenceFile, setReferenceFile] = useState<MediaFile | null>(null);
  const [activeFile, setActiveFile] = useState<string | null>(null);
  const [activeAudio, setActiveAudio] = useState<string | null>(null);
  const [isDragging, setIsDragging] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const audioInputRef = useRef<HTMLInputElement>(null);
  const referenceInputRef = useRef<HTMLInputElement>(null);

  const tabs = [
    { id: 'media', icon: <FolderOpen size={20} />, label: 'Media' },
    { id: 'audio', icon: <Music size={20} />, label: 'Audio' },
    { id: 'reference', icon: <FolderOpen size={20} />, label: 'Reference' },
    { id: 'text', icon: <Type size={20} />, label: 'Text' },
    { id: 'templates', icon: <LayoutTemplate size={20} />, label: 'Templates' },
  ];

  const addFile = useCallback((file: File, fileType: 'video' | 'audio' | 'reference' = 'video') => {
    const url = URL.createObjectURL(file);
    const newMedia: MediaFile = {
      url,
      name: file.name,
      size: formatBytes(file.size),
      type: fileType,
      file,
    };

    if (fileType === 'audio') {
      setAudioFiles(prev => {
        if (prev.some(m => m.name === file.name)) return prev;
        return [newMedia, ...prev];
      });
      setActiveAudio(url);
      onAudioUpload?.(newMedia);
    } else if (fileType === 'reference') {
      setReferenceFile(newMedia);
      onReferenceUpload?.(newMedia);
    } else {
      setMediaFiles(prev => {
        if (prev.some(m => m.name === file.name)) return prev;
        return [newMedia, ...prev];
      });
      setActiveFile(url);
      onVideoUpload(newMedia);
    }
  }, [onVideoUpload, onAudioUpload, onReferenceUpload]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>, fileType: 'video' | 'audio' | 'reference' = 'video') => {
    const file = e.target.files?.[0];
    if (file) addFile(file, fileType);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = () => setIsDragging(false);

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    const file = e.dataTransfer.files?.[0];
    if (file && file.type.startsWith('video/')) {
      addFile(file);
    }
  };

  const handleFileClick = (file: MediaFile) => {
    if (file.type === 'video') {
      setActiveFile(file.url);
      onVideoUpload(file);
    } else if (file.type === 'audio' && onAudioUpload) {
      setActiveAudio(file.url);
      onAudioUpload(file);
    }
  };

  return (
    <aside className="sidebar-container glass-panel">
      <div className="sidebar-tabs">
        {tabs.map(tab => (
          <button
            key={tab.id}
            className={`tab-btn ${activeTab === tab.id ? 'active' : ''}`}
            onClick={() => setActiveTab(tab.id)}
            title={tab.label}
          >
            {tab.icon}
          </button>
        ))}
      </div>

      <div className="sidebar-content">
        <h2 className="section-title">{tabs.find(t => t.id === activeTab)?.label}</h2>

        {activeTab === 'media' && (
          <>
            <div
              className={`upload-area ${isDragging ? 'dragging' : ''}`}
              onClick={() => fileInputRef.current?.click()}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
            >
              <div className="upload-icon-wrap">
                <FolderOpen size={28} className="upload-icon" />
              </div>
              <p className="upload-hint">Drop video here or <span className="upload-link">browse</span></p>
              <p className="upload-formats">MP4, MOV, WebM, AVI</p>
              <input
                type="file"
                accept="video/*"
                ref={fileInputRef}
                style={{ display: 'none' }}
                onChange={e => handleFileChange(e, 'video')}
              />
            </div>

            {mediaFiles.length > 0 && (
              <div className="media-list">
                <p className="media-list-label">Media Files</p>
                {mediaFiles.map(file => (
                  <div
                    key={file.url}
                    className={`media-item ${activeFile === file.url ? 'active' : ''}`}
                    onClick={() => handleFileClick(file)}
                  >
                    <div className="media-thumb">
                      <Film size={16} />
                    </div>
                    <div className="media-info">
                      <span className="media-name" title={file.name}>{file.name}</span>
                      <span className="media-size">{file.size}</span>
                    </div>
                    {activeFile === file.url && (
                      <CheckCircle2 size={16} className="media-active-icon" />
                    )}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'audio' && (
          <>
            <div
              className={`upload-area ${isDragging ? 'dragging' : ''}`}
              onClick={() => audioInputRef.current?.click()}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={(e) => {
                e.preventDefault();
                setIsDragging(false);
                const file = e.dataTransfer.files?.[0];
                if (file && file.type.startsWith('audio/')) {
                  addFile(file, 'audio');
                }
              }}
            >
              <div className="upload-icon-wrap" style={{ background: 'rgba(167, 139, 250, 0.15)', color: '#a78bfa' }}>
                <Music size={28} className="upload-icon" />
              </div>
              <p className="upload-hint">Drop audio here or <span className="upload-link">browse</span></p>
              <p className="upload-formats">MP3, WAV, AAC</p>
              <input
                type="file"
                accept="audio/*"
                ref={audioInputRef}
                style={{ display: 'none' }}
                onChange={e => handleFileChange(e, 'audio')}
              />
            </div>

            {audioFiles.length > 0 && (
              <div className="media-list">
                <p className="media-list-label">Music & Beats</p>
                {audioFiles.map(file => (
                  <div
                    key={file.url}
                    className={`media-item ${activeAudio === file.url ? 'active' : ''}`}
                    onClick={() => {
                      setActiveAudio(file.url);
                      if (onAudioUpload) onAudioUpload(file);
                    }}
                  >
                    <div className="media-thumb" style={{ background: 'rgba(167, 139, 250, 0.2)' }}>
                      <Music size={16} color="#a78bfa" />
                    </div>
                    <div className="media-info">
                      <span className="media-name" title={file.name}>{file.name}</span>
                      <span className="media-size">{file.size}</span>
                    </div>
                    {activeAudio === file.url && (
                      <CheckCircle2 size={16} className="media-active-icon" />
                    )}
                  </div>
                ))}
              </div>
            )}
          </>
        )}

        {activeTab === 'reference' && (
          <>
            <div
              className={`upload-area ${isDragging ? 'dragging' : ''}`}
              onClick={() => referenceInputRef.current?.click()}
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={(e) => {
                e.preventDefault();
                setIsDragging(false);
                const file = e.dataTransfer.files?.[0];
                if (file && file.type.startsWith('video/')) {
                  addFile(file, 'reference');
                }
              }}
            >
              <div className="upload-icon-wrap" style={{ background: 'rgba(0, 242, 254, 0.15)', color: '#00f2fe' }}>
                <FolderOpen size={28} className="upload-icon" />
              </div>
              <p className="upload-hint">Drop reference video <span className="upload-link">browse</span></p>
              <p className="upload-formats">MP4, MOV, WEBM (AI will mimic its style)</p>
              <input
                type="file"
                accept="video/*"
                ref={referenceInputRef}
                style={{ display: 'none' }}
                onChange={e => handleFileChange(e, 'reference')}
              />
            </div>

            {referenceFile && (
              <div className="media-list">
                <p className="media-list-label">Style Reference Target</p>
                <div className="media-item active">
                  <div className="media-thumb" style={{ background: 'rgba(0, 242, 254, 0.2)' }}>
                    <FolderOpen size={16} color="#00f2fe" />
                  </div>
                  <div className="media-info">
                    <span className="media-name" title={referenceFile.name}>{referenceFile.name}</span>
                    <span className="media-size">{referenceFile.size}</span>
                  </div>
                  <CheckCircle2 size={16} className="media-active-icon" style={{ color: '#00f2fe' }} />
                </div>
              </div>
            )}
          </>
        )}

        {activeTab !== 'media' && activeTab !== 'audio' && activeTab !== 'reference' && (
          <div className="coming-soon">
            <div className="coming-soon-icon">
              {tabs.find(t => t.id === activeTab)?.icon}
            </div>
            <p>Coming Soon</p>
            <span>This panel is under development</span>
          </div>
        )}
      </div>
    </aside>
  );
};

export default Sidebar;
